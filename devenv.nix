{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  packages = [
    pkgs.git
    pkgs.bun
    pkgs.act
  ];

  languages = {
    python = {
      enable = true;
      uv = {
        enable = true;
      };
    };
    javascript.bun = {
      enable = true;
      install.enable = true;
    };
  };
}
