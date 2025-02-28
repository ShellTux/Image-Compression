{
  description = "A Nix-flake-based Multimedia development environment";

  inputs.nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*.tar.gz";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          venvDir = ".venv";
          packages = with pkgs; [ python311 ] ++
            (with pkgs.python311Packages; [
              bpython
              matplotlib
              numpy
              opencv-python
              pip
              scipy
              venvShellHook
            ])
            ++ [
                pkgs.ffmpeg
                pkgs.gnumake
                pkgs.imv
                pkgs.pandoc
                pkgs.qiv
                pkgs.texliveFull
            ];
        };

        pedro = pkgs.mkShell {
          venvDir = ".venv";
          packages = with pkgs; [ python311 ] ++
            (with pkgs.python311Packages; [
              matplotlib
              numpy
              opencv-python
              pip
              scipy
              venvShellHook
            ])
            ++ [
                pkgs.ffmpeg
                pkgs.gnumake
                pkgs.pandoc
                pkgs.texliveFull
            ];
        };
      });
    };
}
