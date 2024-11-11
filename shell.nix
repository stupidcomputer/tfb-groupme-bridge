{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    nativeBuildInputs = with pkgs; [
        buildPackages.python311Packages.django
        buildPackages.python311Packages.requests
    ];
}