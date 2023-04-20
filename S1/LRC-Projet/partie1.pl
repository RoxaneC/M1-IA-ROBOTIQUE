%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%                               %%
%%           Partie 1            %%
%%                               %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% CODE DONNÉ
% Définition des identificateurs

cnamea(personne).
cnamea(livre).
cnamea(objet).
cnamea(sculpture).
cnamea(anything).
cnamea(nothing).

cnamena(auteur).
cnamena(editeur).
cnamena(sculpteur).
cnamena(parent).

iname(michelAnge).
iname(david).
iname(sonnets).
iname(vinci).
iname(joconde).

rname(aCree).
rname(aEcrit).
rname(aEdite).
rname(aEnfant).


% T-Box

equiv(sculpteur,and(personne,some(aCree,sculpture))).
equiv(auteur,and(personne,some(aEcrit,livre))).
equiv(editeur,and(personne,and(not(some(aEcrit,livre)),some(aEdite,livre)))).
equiv(parent,and(personne,some(aEnfant,anything))).

% Représentation de la T-Box telle qu'elle sera utilisée dans le programme
% [(sculpteur,and(personne,some(aCree,sculpture))), (auteur,and(personne,some(aEcrit,livre))),(editeur,and(personne,and(not(some(aEcrit,livre)),some(aEdite,livre)))),(parent,and(personne,some(aEnfant,anything)))]


% A-Box

inst(michelAnge,personne).
inst(david,sculpture).
inst(sonnets,livre).
inst(vinci,personne).
inst(joconde,objet).

instR(michelAnge, david, aCree).
instR(michelAnge, sonnets, aEcrit).
instR(vinci, joconde, aCree).

% Représentation de la A-Box des assertions de concepts telle qu'elle sera utilisée dans le programme
% [(michelAnge,personne), (david,sculpture), (sonnets,livre),(vinci,personne), (joconde,objet)]
%
% Représentation de la A-Box des assertions de rôles telle qu'elle sera utilisée dans le programme
% [(michelAnge, david, aCree), (michelAnge, sonnet, aEcrit),(vinci,joconde, aCree)]
%%


% Correction syntaxique et sémantique
% Permet de vérifier que les concepts, les rôles et les instances existent dans nos Box

concept(C) :-	cnamea(C), !.
concept(C) :-	cnamena(C), !.
concept(not(C)) :-	concept(C), !.
concept(or(C1,C2)) :-	concept(C1), concept(C2), !.
concept(and(C1,C2)) :-	concept(C1), concept(C2), !.
concept(some(R,C)) :-	role(R), concept(C), !.
concept(all(R,C)) :-	role(R), concept(C), !.

instance(I) :-	iname(I), !.
role(R) :-	rname(R), !.


% On verifie qu'il n'y a pas de cycle

autoref(C, C).
autoref(C, equiv(C,D)) :- remplace(D,DA), autoref(C,DA), !.
autoref(C, and(A,B)) :-	autoref(C,A), autoref(C,B), !.
autoref(C, or(A,B)) :-	autoref(C,A), autoref(C,B), !.
autoref(C, some(R,B)) :-	autoref(C,B), !.
autoref(C, all(R,B)) :-	autoref(C,B), !.


%%% Traitements

% Remplace les concepts non atomiques par une definition formée uniquement de concepts atomiques

remplace(CA, CA) :- cnamea(CA), !.
remplace(CNA, DCA) :- equiv(CNA, D), remplace(D, DCA), !.
remplace(not(CNA), not(CA)) :- 	remplace(CNA, CA), !.
remplace(or(CNA1, CNA2), or(CA1, CA2)) :- 	remplace(CNA1, CA1), remplace(CNA2, CA2), !.
remplace(and(CNA1, CNA2), and(CA1, CA2)) :- 	remplace(CNA1, CA1), remplace(CNA2, CA2), !.
remplace(some(R, CNA), some(R, CA)) :- 	remplace(CNA, CA), !.
remplace(all(R, CNA), all(R, CA)) :- 	remplace(CNA, CA), !.


% Traitement de la T-Box comme demandé :
% - développement des concepts en formes atomiques
% - verification sémentique et syntaxique
% - mise sous nnf

traitement_Tbox([], []).
traitement_Tbox([(C,D) | Tbox], [(NC,ND) | L]) :- 	concept(C), concept(D), not(autoref(C,D)),
													remplace(C,CA), remplace(D,DA),
													nnf(CA, NC), nnf(DA,ND),
													traitement_Tbox(Tbox, L), !.


% Traitement de la A-Box des assertions de concepts comme demandé :
% - développement des concepts en formes atomiques
% - verification sémentique et syntaxique
% - mise sous nnf

traitement_AboxI([], []).
traitement_AboxI([(I,C) | AboxI], [(I,NC) | L] ) :-	instance(I), concept(C),
													remplace(C,CA),
													nnf(CA, NC),
													traitement_AboxI(AboxI, L), !.


% Traitement de la A-Box des assertions de rôles comme demandé :
% - verification sémentique et syntaxique

traitement_AboxR([]).
traitement_AboxR([(I1,I2,R) | AboxR]) :-	instance(I1), instance(I2), role(R),
											traitement_AboxR(AboxR), !.
