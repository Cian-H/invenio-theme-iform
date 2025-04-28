{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  packages = [pkgs.git];

  languages.python = {
    enable = true;
    uv = {
      enable = true;
    };
  };
}
