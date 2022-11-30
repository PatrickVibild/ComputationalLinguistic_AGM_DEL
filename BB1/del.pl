

:- use_module(cnfFOL, [cnf/2]).

:- use_module(holeSemantics, [holeSemantics/2]).

holeCNF(Sentence, CNF) :-
   holeSemantics(Sentence, Sems),
   head(Sems, F_sems),
   cnf(F_sems, CNF).

head([H|_], H).

accExtractPN([H|T], A, R) :-
    holeSemantics:lexEntry(pn,[symbol:Sym,syntax:[H]]),
    accExtractPN(T, [Sym|A], R).

accExtractPN([_|T], A, R) :-
    accExtractPN(T, A, R).

accExtractPN([], PN, PN).

extractPN(Sentence, R) :-
    accExtractPN(Sentence, [], PN),
    rev(PN,R).


accRev([H|T],A,R) :-
    accRev(T,[H|A],R).
accRev([],A,A).

rev(L,R) :- accRev(L,[],R).

belief([Agent,belief,that|Question],Sym,Question) :-
    holeSemantics:lexEntry(pn,[symbol:Sym,syntax:[Agent]]).
