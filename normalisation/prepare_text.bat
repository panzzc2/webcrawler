@echo off
for %%s in (cleanUnwantedChars.pl) do (
for %%m in (1 2 3 4 5 6 7 8 9 10 11 12) do @(perl %%s 2014 %%m utusan)
)
echo on
