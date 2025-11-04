{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        packages =
          pkgs: with pkgs; [
            python3
            python3Packages.pip
            python3Packages.unittest-xml-reporting
            python3Packages.pyyaml
          ];
        libs =
          pkgs: with pkgs; [
            zstd
            stdenv.cc.cc
          ];
      in
      rec {
        devShell = pkgs.mkShell {
          buildInputs = packages pkgs;
          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath (libs pkgs)}:$LD_LIBRARY_PATH
          '';
        };
        defaultPackage = devShell;
      }
    );
}
