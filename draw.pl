:- set_prolog_flag(verbose, silent).

:- initialization main.

main :-
    format('Example script~n'),
    current_prolog_flag(argv, Argv),
    format('Called with ~q~n', [Argv]),
    load_data(Argv),
    tikz:export_tikz([]),
    halt.
main :-
    halt(1).