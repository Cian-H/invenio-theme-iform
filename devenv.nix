{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  packages = [
    pkgs.git
    pkgs.act
  ];

  languages.python = {
    enable = true;
    uv = {
      enable = true;
    };
  };
}
