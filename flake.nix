{
  description = "A Nix-flake-based Multimedia development environment";

  inputs.nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*.tar.gz";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f rec {
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312.withPackages (pp: [
          pp.ipython
          pp.matplotlib
          pp.numpy
          pp.opencv-python
          pp.scipy
        ]);
        pythonPackages = pkgs.python312Packages;
      });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs, python, pythonPackages }: {
        default = pkgs.mkShell {
          venvDir = ".venv";
          packages = [
            python
            pythonPackages.bpython
            pythonPackages.pip
            pythonPackages.venvShellHook
            pkgs.ffmpeg
            pkgs.gnumake
            pkgs.imv
            pkgs.pandoc
            pkgs.pandoc-include
            pkgs.qiv
            pkgs.texliveFull
          ];
        };

        pedro = pkgs.mkShell {
          venvDir = ".venv";
          packages = [
            python
            pythonPackages.pip
            pythonPackages.venvShellHook
            pkgs.ffmpeg
            pkgs.gnumake
            pkgs.pandoc
            pkgs.pandoc-include
            pkgs.texliveFull
          ];
        };
      });
    };
}
