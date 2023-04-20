
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%                               %%
%%           Partie 3            %%
%%                               %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

compteur(1).

%% CODE DONNÉ
troisieme_etape(Abi,Abr) :-	tri_Abox(Abi,Lie,Lpt,Li,Lu,Ls),
							resolution(Lie,Lpt,Li,Lu,Ls,Abr), nl,
							write('Youpiiiiii, on a demontre la proposition initiale !!!').
							
%%%


% Tri de la A_Box étendue en fonction de la relation considérée
tri_Abox([], Lie, Lpt, Li, Lu, Ls).
tri_Abox([ (I,some(R,C)) | Abi], [ (I,some(R,C)) | Lie], Lpt, Li, Lu, Ls) :-	tri_Abox(Abi, Lie, Lpt, Li, Lu, Ls), !.
tri_Abox([ (I,all(R,C)) | Abi], Lie, [ (I,all(R,C)) | Lpt], Li, Lu, Ls) :-		tri_Abox(Abi, Lie, Lpt, Li, Lu, Ls), !.
tri_Abox([ (I,and(C1,C2)) | Abi], Lie, Lpt, [ (I,and(C1,C2)) | Li], Lu, Ls) :-	tri_Abox(Abi, Lie, Lpt, Li, Lu, Ls), !.
tri_Abox([ (I,or(C1,C2)) | Abi], Lie, Lpt, Li, [ (I,or(C1,C2)) | Lu], Ls) :-	tri_Abox(Abi, Lie, Lpt, Li, Lu, Ls), !.
tri_Abox([ (I,C) | Abi], Lie, Lpt, Li, Lu, [ (I,C) | Ls]) :-					tri_Abox(Abi, Lie, Lpt, Li, Lu, Ls), !.
tri_Abox([ (I,not(C)) | Abi], Lie, Lpt, Li, Lu, [ (I,not(C)) | Ls]) :-			tri_Abox(Abi, Lie, Lpt, Li, Lu, Ls), !.



%%% Prédicats de résolution

% Résolution par les différentes étapes

resolution(Lie, Lpt, Li, Lu, Ls, Abr) :-	pas_clash(Ls), complete_some(Lie, Lpt, Li, Lu, Ls, Abr), !.
resolution([], Lpt, Li, Lu, Ls, Abr) :-	pas_clash(Ls), transformation_and([], Lpt, Li, Lu, Ls, Abr), !.
resolution([], Lpt, [], Lu, Ls, Abr) :-	pas_clash(Ls), deduction_all([], Lpt, [], Lu, Ls, Abr), !.
resolution([], [], [], Lu, Ls, Abr):-	pas_clash(Ls), transformation_or([], [], [], Lu, Ls, Abr), !.
resolution([], [], [], [], Ls, Abr):-	pas_clash(Ls), !.


% Vérifie la présence d'un clash

pas_clash([]).
pas_clash([(I,C) | Ls]) :-	nnf(not(C), NC), not(member((I,NC), Ls)), pas_clash(Ls).


% Cas "il existe"

complete_some([ (I1,some(R,C)) | Lie], Lpt, Li, Lu, Ls, Abr) :-	genere(I2),		% génération d'un nom d'instance
			% modifie en conséquence les listes concernées
			evolue((I2,C), Lie, Lpt, Li, Lu, Ls, Lie1, Lpt1, Li1, Lu1, Ls1),
			% affiche l'évolution à cette étape
			affiche_evolution_Abox(Ls, [ (I1,some(R,C)) | Lie], Lpt, Li, Lu, Abr, Ls1, Lie1, Lpt1, Li1, Lu1, [ (I1, I2, R) | Abr]),
			% retour à la résolution avec les nouvelles listes
			resolution(Lie1, Lpt1, Li1, Lu1, Ls1, [ (I1, I2, R) | Abr]), !.


% Cas "et"

transformation_and(Lie, Lpt, [ (I,and(C1,C2)) | Li], Lu, Ls, Abr) :- 
			% modifie en conséquence les listes concernées
			evolue([(I,C1), (I,C2)], Lie, Lpt, Li, Lu, Ls1, Lie1, Lpt1, Li1, Lu1, Ls1),
			% affiche l'évolution à cette étape
			affiche_evolution_Abox(Ls, Lie, Lpt, [ (I,and(C1,C2)) | Li], Lu, Abr, Ls1, Lie1, Lpt1, Li1, Lu1, Abr),
			% retour à la résolution avec les nouvelles listes
			resolution(Lie1, Lpt1, Li1, Lu1, Ls1, Abr), !.


% Cas "pour tout"

deduction_all(Lie, [ (I1,all(R,C)) | Lpt], Li, Lu, Ls, Abr) :- 	
			member((I1,I2,R), Abr),		% on regarde si une relation de rôle existe dans la A-Box
			% modifie en conséquence les listes concernées
			evolue((I2,C), Lie, Lpt, Li, Lu, Ls, Lie1, Lpt1, Li1, Lu1, Ls1),
			% affiche l'évolution à cette étape
			affiche_evolution_Abox(Ls, Lie, [ (I1,all(R,C)) | Lpt], Li, Lu, Abr, Ls1, Lie1, Lpt1, Li1, Lu1, Abr),
			% retour à la résolution avec les nouvelles listes
			resolution(Lie1, Lpt, Li1, Lu1, Ls1, Abr), !.


% Cas "ou"

transformation_or(Lie, Lpt, Li, [ (I,or(C1,C2)) | Lu], Ls, Abr) :-	
			% modifie en conséquence les listes concernées (deux noeuds)
			evolue((I,C1), Lie, Lpt, Li, Lu, Ls, Lie1, Lpt1, Li1, Lu1, Ls1),
			evolue((I,C2), Lie, Lpt, Li, Lu, Ls, Lie2, Lpt2, Li2, Lu2, Ls2),
			% affiche l'évolution à cette étape
			affiche_evolution_Abox(Ls, Lie, Lpt, Li, [ (I,or(C1,C2)) | Lu], Abr, Ls1, Lie1, Lpt1, Li1, Lu1, Abr),
			affiche_evolution_Abox(Ls, Lie, Lpt, Li, [ (I,or(C1,C2)) | Lu], Abr, Ls2, Lie2, Lpt2, Li2, Lu2, Abr),
			% retour à la résolution avec les nouvelles listes (deux noeuds)
			resolution(Lie1, Lpt1, Li1, Lu1, Ls1, Abr),
			resolution(Lie2, Lpt2, Li2, Lu2, Ls2, Abr), !.


% Modification et mise à jour des listes selon la relation considérée
% Appel récursif dans le cas d'une liste en premier argument
evolue([], Lie, Lpt, Li, Lu, Ls, Lie, Lpt, Li, Lu, Ls).
evolue([Elem | L], Lie, Lpt, Li, Lu, Ls, Lie1, Lpt1, Li1, Lu1, Ls1) :- 
			evolue(Elem, Lie, Lpt, Li, Lu, Ls, Lie2, Lpt2, Li2, Lu2, Ls2),
			evolue(L, Lie2, Lpt2, Li2, Lu2, Ls2, Lie1, Lpt1, Li1, Lu1, Ls1), !.

evolue((I,some(R,C)), Lie, Lpt, Li, Lu, Ls, Lie1, Lpt, Li, Lu, Ls) :- 	concat([ (I,some(R,C)) ], Lie, Lie1), !.
evolue((I,all(R,C)), Lie, Lpt, Li, Lu, Ls, Lie, Lpt1, Li, Lu, Ls) :- 	concat([ (I,all(R,C)) ], Lpt, Lpt1), !.
evolue((I,and(C1,C2)), Lie, Lpt, Li, Lu, Ls, Lie, Lpt, Li1, Lu, Ls) :- 	concat([ (I,and(C1,C2)) ], Li, Li1), !.
evolue((I,or(C1,C2)), Lie, Lpt, Li, Lu, Ls, Lie, Lpt, Li, Lu1, Ls) :- 	concat([ (I,or(C1,C2)) ], Lu, Lu1), !.
evolue((I,C), Lie, Lpt, Li, Lu, Ls, Lie, Lpt, Li, Lu, Ls1) :- 			concat([ (I,C) ], Ls, Ls1), !.
evolue((I,not(C)), Lie, Lpt, Li, Lu, Ls, Lie, Lpt, Li, Lu, Ls1) :- 		concat([ (I,not(C)) ], Ls, Ls1), !.


%%% Affichage

% Permet d'afficher les modifications entre les différentes étapes

affiche_evolution_Abox(Ls1, Lie1, Lpt1, Li1, Lu1, Abr1, Ls2, Lie2, Lpt2, Li2, Lu2, Abr2):-
	write('Etat Départ :'),nl,
	write('- Ls : '), nl, affiche(Ls1),
	write('- Lie : '), nl, affiche(Lie1),
	write('- Lpt : '), nl, affiche(Lpt1),
	write('- Li : '), nl, affiche(Li1),
	write('- Lu : '), nl, affiche(Lu1),
	write('- Abr : '), nl, affiche(Abr1),
	nl,
	write('Etat Arrivée :'),nl,
	write('- Ls : '), nl, affiche(Ls2),
	write('- Lie : '), nl, affiche(Lie2),
	write('- Lpt : '), nl, affiche(Lpt2),
	write('- Li : '), nl, affiche(Li2),
	write('- Lu : '), nl, affiche(Lu2),
	write('- Abr : '), nl, affiche(Abr2),
	nl, write('Fin de l étape.').


% Permet d'afficher les différentes relations entre concepts, rôles et instances

% récursivité d'affichage sur les listes
affiche([]) :-	nl.
affiche([Elem | L]) :-	affiche(Elem), nl,
						affiche(L), !.
% affichage des concepts
affiche(C) :- write(C), !.
affiche((I1,I2,R)) :-	write('<'), write(I1), write(','), write(I2), write('> : '), write(R), !.
affiche((I,C)) :-	write(I), write(' : '), affiche(C), !.
affiche((I,not(C))) :-	write(I), write(' : ¬('), affiche(C), write(')'), !.
affiche((I,some(R,C))) :-	write(I), write(' : ∃ '),
							write(R), write('.('), affiche(C), write(')'), !.
affiche((I,all(R,C))) :-	write(I), write(' : ∀ '),
							write(R), write('.('), affiche(C), write(')'), !.
affiche((I,and(C1,C2))) :-	write(I), write(' : ('),
							affiche(C1), write(' ⊓ '), affiche(C2), write(')'), !.
affiche((I,or(C1,C2))) :-	write(I), write(' : ('),
							affiche(C1), write(' ⊔ '), affiche(C2), write(')'), !.
