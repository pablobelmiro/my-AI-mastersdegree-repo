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
    echo "Ambiente para Motor de Regex Thompson carregado!"
    echo "Comando: runghc Main-3-regular-expression.hs \"regex\" [palavra]"
  '';
}
