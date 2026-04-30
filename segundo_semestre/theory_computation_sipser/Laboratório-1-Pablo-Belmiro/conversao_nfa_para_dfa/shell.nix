{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # buildInputs: lista os pacotes necessários para o projeto
  buildInputs = [
    (pkgs.haskellPackages.ghcWithPackages (p: [
      p.yaml
    ]))
  ];

  # instruções que aparecem ao entrar no ambiente
  shellHook = ''
    echo "Aluno: Pablo Belmiro"
    echo "dependências carregadas: GHC + Data.Yaml"
    echo "comando para executar o código de conversão dos autômatos: runghc Main-2-1-conversao-automatos.hs nfae.yaml"
  '';
}
