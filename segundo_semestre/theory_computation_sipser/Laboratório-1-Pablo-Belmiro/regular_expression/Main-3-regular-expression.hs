{-# LANGUAGE DeriveGeneric #-}

import GHC.Generics (Generic)
import Data.Yaml (ToJSON, encodeFile)
import Data.List (nub, sort)
import System.Environment (getArgs)
import Data.Char (isAlphaNum)

-- 1. dados, modelo do autômato
data Transicao = Transicao {
    from   :: String, 
    symbol :: String, 
    to     :: [String]
} deriving (Show, Generic, Eq)

instance ToJSON Transicao

data Automato = Automato {
    type_         :: String, 
    alphabet      :: [String],
    states        :: [String],
    initial_state :: String,
    final_states  :: [String],
    transitions   :: [Transicao]
} deriving (Show, Generic, Eq)

instance ToJSON Automato

-- 2. definição da expressao regular, árvore sintática
data Regex = Letra Char
           | Vazio --epsilon
           | Concat Regex Regex
           | Alternativa Regex Regex
           | Repetir Regex   -- fecho de Kleene*
           | UmOuMais Regex  -- operador +
           | Opcional Regex  -- operador ?
           deriving (Show)

-- 3. parser, transforma texto em estrutura de dados, método "descida recursiva"
parseRegex :: String -> Regex
parseRegex s = fst (expressao s)

expressao :: String -> (Regex, String)
expressao s =
    let (r1, restos1) = termo s
    in case restos1 of
        ('|':restos2) -> let (r2, restos3) = expressao restos2 in (Alternativa r1 r2, restos3)
        _             -> (r1, restos1)

termo :: String -> (Regex, String)
termo s =
    let (r1, restos1) = fator s
    in case restos1 of
        (c:_) | isAlphaNum c || c == '(' -> 
            let (r2, restos2) = termo restos1 in (Concat r1 r2, restos2)
        _ -> (r1, restos1)

fator :: String -> (Regex, String)
fator s =
    let (r, restos1) = base s
    in case restos1 of
        ('*':restos2) -> (Repetir r, restos2)
        ('+':restos2) -> (UmOuMais r, restos2)
        ('?':restos2) -> (Opcional r, restos2)
        _             -> (r, restos1)

base :: String -> (Regex, String)
base ('(':restos) =
    let (r, restos1) = expressao restos
    in case restos1 of
        (')':restos2) -> (r, restos2)
        _             -> error "Erro: parênteses faltando"
base (c:restos) | isAlphaNum c = (Letra c, restos)
base _ = error "Erro: caractere inválido"

-- 4. construção de Thompson, criação do Autômato
thompson :: Regex -> Int -> (Int, Int, [Transicao], Int)
thompson (Letra c) idAtual = 
    let idFim = idAtual + 1
    in (idAtual, idFim, [Transicao (show idAtual) [c] [show idFim]], idAtual + 2)

thompson Vazio idAtual = 
    let idFim = idAtual + 1
    in (idAtual, idFim, [Transicao (show idAtual) "epsilon" [show idFim]], idAtual + 2)

thompson (Concat r1 r2) idAt =
    let (i1, f1, t1, id2) = thompson r1 idAt
        (i2, f2, t2, id3) = thompson r2 id2
        ligacao = Transicao (show f1) "epsilon" [show i2]
    in (i1, f2, t1 ++ t2 ++ [ligacao], id3)

thompson (Alternativa r1 r2) idAt =
    let sInicio = idAt
        (i1, f1, t1, id2) = thompson r1 (idAt + 1)
        (i2, f2, t2, id3) = thompson r2 id2
        sFim = id3
        novas = [ Transicao (show sInicio) "epsilon" [show i1, show i2]
                , Transicao (show f1) "epsilon" [show sFim]
                , Transicao (show f2) "epsilon" [show sFim] ]
    in (sInicio, sFim, t1 ++ t2 ++ novas, id3 + 1)

thompson (Repetir r) idAt =
    let sInicio = idAt
        (i, f, t, id2) = thompson r (idAt + 1)
        sFim = id2
        novas = [ Transicao (show sInicio) "epsilon" [show i, show sFim]
                , Transicao (show f) "epsilon" [show i, show sFim] ]
    in (sInicio, sFim, t ++ novas, id2 + 1)

thompson (UmOuMais r) idAt = thompson (Concat r (Repetir r)) idAt
thompson (Opcional r) idAt = thompson (Alternativa r Vazio) idAt

-- 5. simulador do automato ou reconhecimento das palavras
pegarFechoEpsilon :: [String] -> [Transicao] -> [String]
pegarFechoEpsilon estados listaT =
    let novos = nub $ estados ++ concat [ destinos | Transicao onde simb destinos <- listaT, onde `elem` estados, simb == "epsilon" ]
    in if length novos == length estados then estados else pegarFechoEpsilon novos listaT

mover :: [String] -> Char -> [Transicao] -> [String]
mover estados letra listaT =
    let destinos = concat [ ondeIr | Transicao onde simb ondeIr <- listaT, onde `elem` estados, simb == [letra] ]
    in pegarFechoEpsilon (nub destinos) listaT

testarPalavra :: Automato -> String -> Bool
testarPalavra aut palavra =
    let 
        transicoes = transitions aut
        estadosIniciais = pegarFechoEpsilon [initial_state aut] transicoes
        estadosFinaisAlcancados = foldl (\est letra -> mover est letra transicoes) estadosIniciais palavra
    in any (`elem` final_states aut) estadosFinaisAlcancados

main :: IO ()
main = do
    parametros <- getArgs
    case parametros of
        [regexTexto, palavra] -> do
            let nfae = montarAutomato (parseRegex regexTexto)
            if testarPalavra nfae palavra
                then putStrLn "Status: PALAVRA ACEITA"
                else putStrLn "Status: PALAVRA REJEITADA"

        [regexTexto] -> do
            let nfae = montarAutomato (parseRegex regexTexto)
            encodeFile "regex_nfae.yaml" nfae
            putStrLn $ "Sucesso: Autômato gerado para '" ++ regexTexto ++ "'"

        _ -> putStrLn "Uso: runghc Main-3-regular-expression.hs \"regex\" [palavra]"

montarAutomato :: Regex -> Automato
montarAutomato regex =
    let (ini, fim, trans, _) = thompson regex 0
        todosEstados = sort $ nub $ concat [ [onde] ++ irPara | Transicao onde _ irPara <- trans ]
        todosSimbolos = nub [ simb | Transicao _ simb _ <- trans, simb /= "epsilon" ]
    in Automato "nfae" todosSimbolos todosEstados (show ini) [show fim] trans
