{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    nativeBuildInputs = with pkgs; [
        buildPackages.python311Packages.requests
        buildPackages.python311Packages.flask
    ];
}