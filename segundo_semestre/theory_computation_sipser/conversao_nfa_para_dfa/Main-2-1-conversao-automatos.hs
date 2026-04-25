{-# LANGUAGE DeriveGeneric #-}

import System.Environment (getArgs)
import Data.Yaml (FromJSON, ToJSON, decodeFileEither, encodeFile)
import GHC.Generics (Generic)
import Data.List (nub, sort, intercalate)

-- 1. definição dos dados
data Transicao = Transicao {
    from   :: String,
    symbol :: String,
    to     :: [String]
} deriving (Show, Generic, Eq)

instance FromJSON Transicao
instance ToJSON Transicao

data Automato = Automato {
    type_         :: String, 
    alphabet      :: [String],
    states        :: [String],
    initial_state :: String,
    final_states  :: [String],
    transitions   :: [Transicao]
} deriving (Show, Generic, Eq)

instance FromJSON Automato
instance ToJSON Automato

-- 2. funções de apoio
buscarDestinos :: String -> String -> [Transicao] -> [String]
buscarDestinos estadoProcurado simboloProcurado listaTotal =
    concat [ t_to | Transicao t_from t_sym t_to <- listaTotal, t_from == estadoProcurado, t_sym == simboloProcurado ]

-- professor, essa é a minha função de cálculo de ponto fixo, garantindo término da verificação das transições
pegarFecho :: [String] -> [Transicao] -> [String]
pegarFecho estados listaT =
    let novos = nub $ estados ++ concat [ buscarDestinos e "epsilon" listaT | e <- estados ]
    in if length novos == length estados then estados else pegarFecho novos listaT

-- 3. parte: NFA-epsilon -> NFA removendo epsilon
removerEpsilon :: Automato -> Automato
removerEpsilon nfa =
    let
        listaT = transitions nfa
        alfabeto = alphabet nfa
        
        -- loop: para cada estado e símbolo, o novo destino é: Fecho(Destino(Fecho(Estado)))
        novasTrans = [ Transicao s simb (nub $ sort $ pegarFecho destinos listaT)
                     | s <- states nfa,
                     simb <- alfabeto,
                     let fechoOrigem = pegarFecho [s] listaT,
                     let destinos = concat [ buscarDestinos e simb listaT | e <- fechoOrigem ],
                     not (null destinos) ]
        
        -- um estado é final se o epsilon dele contém algum final original
        novosFinais = [ s | s <- states nfa, any (`elem` final_states nfa) (pegarFecho [s] listaT) ]
    in
        nfa { transitions = novasTrans, final_states = novosFinais }

-- 4. parte b: NFA -> DFA subset construction
construcaoSubconjuntos :: Automato -> Automato
construcaoSubconjuntos nfa =
    let
        -- função recursiva que explora os conjuntos de estados
        resolver vistos [] transAcumuladas = (vistos, transAcumuladas)
        resolver vistos (atual:resto) transAcumuladas
            | atual `elem` vistos = resolver vistos resto transAcumuladas
            | otherwise =
                let
                    -- para cada letra, vê para onde o conjunto vai
                    proximo simb = nub $ sort $ concat [ buscarDestinos e simb (transitions nfa) | e <- atual ]
                    
                    destinosSimbolos = [ (s, proximo s) | s <- alphabet nfa, not (null (proximo s)) ]
                    
                    -- vria as transições do DFA usando os nomes dos conjuntos
                    novas = [ Transicao (intercalate "," atual) s [intercalate "," d] | (s, d) <- destinosSimbolos ]
                    novos  = [ d | (_, d) <- destinosSimbolos, d `notElem` vistos ]
                in 
                    resolver (atual:vistos) (resto ++ novos) (transAcumuladas ++ novas)

        -- inicia a exploração a partir do estado inicial
        conjInicial = sort [initial_state nfa]
        (todosConjuntos, totalTrans) = resolver [] [conjInicial] []
        
        -- define quem são os estados e os finais no DFA
        mapNome c = intercalate "," c
        dfaStates = map mapNome todosConjuntos
        dfaFinais = [ mapNome c | c <- todosConjuntos, any (`elem` final_states nfa) c ]
    in
        nfa { 
            type_ = "dfa",
            initial_state = mapNome conjInicial,
            states = dfaStates,
            final_states = dfaFinais,
            transitions = totalTrans
        }

main :: IO ()
main = do
    args <- getArgs
    case args of
        [arquivo] -> do
            resultado <- decodeFileEither arquivo
            case resultado of
                Left erro -> print erro
                Right nfae -> do
                    -- passo 1: NFA-epsilon -> NFA
                    let nfa = removerEpsilon nfae
                    -- passo 2: NFA -> DFA
                    let dfa = construcaoSubconjuntos nfa
                    
                    encodeFile "dfa.yaml" dfa
                    putStrLn "Conversão Finalizada: NFA-epsilon -> NFA -> DFA"
        _ -> putStrLn "Uso: runghc Main-2-1-conversao-automatos.hs <arquivo.yaml>"
