
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%                               %%
%%           Partie 2            %%
%%                               %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% CODE DONNÉ
% Definition du programme
programme :- 	premiere_etape(Tbox,Abi,Abr),
				deuxieme_etape(Abi,Abi1,Tbox),
				troisieme_etape(Abi1,Abr).
%%


%%% Première étape

% Création des listes codants les A-Box et T-Box d'après les prédicats de la partie 1

premiere_etape(Tbox,Abi,Abr):- 	setof((C, D), equiv(C, D), T), traitement_Tbox(T,Tbox),
								setof((I, C), inst(I, C), Ai), traitement_AboxI(Ai,Abi),
								setof((I1, I2, R), instR(I1, I2, R), Abr), traitement_AboxR(Abr), !.


%%% Deuxième étape

%% CODE DONNÉ
deuxieme_etape(Abi,Abi1,Tbox) :- 	saisie_et_traitement_prop_a_demontrer(Abi,Abi1,Tbox).

saisie_et_traitement_prop_a_demontrer(Abi,Abi1,Tbox) :-
			nl, write('Entrez le numero du type de proposition que vous voulez demontrer :'), nl, 
			write('1 Une instance donnee appartient a un concept donne.'), nl,
			write('2 Deux concepts n"ont pas d"elements en commun(ils ont une intersection vide).'), nl, read(R), 
			suite(R,Abi,Abi1,Tbox).

suite(1,Abi,Abi1,Tbox) :- 	acquisition_prop_type1(Abi,Abi1,Tbox), !.
suite(2,Abi,Abi1,Tbox) :- 	acquisition_prop_type2(Abi,Abi1,Tbox), !.
suite(R,Abi,Abi1,Tbox) :- 	nl, write('Cette reponse est incorrecte.'), nl,
			saisie_et_traitement_prop_a_demontrer(Abi,Abi1,Tbox).
%%


%%% Ajout de propositions aux Box

% Permet l'ajout d'une proposition pour un test du type "I : C" (vérification d'une instance)
% on ajoute la négation du concept dans la A-Box
% (après avoir verifié sa syntaxe et sémentique, et l'avoir mis sous forme atomique et nnf)

acquisition_prop_type1(Abi,Abi1,Tbox) :- 
			nl, write('Entrez le nom de l"instance que vous souhaitez tester :'), nl,
			read(I), instance(I),
			nl, write('Entrez le concept associé que vous souhaitez tester :'), nl,
			read(C), concept(C),
			remplace(C, CA),
			nnf(not(CA), NCA),
			concat(Abi, [(I,NCA)], Abi1), !.


% Permet l'ajout d'une proposition pour un test du type "C1 ⊓ C2 ⊑ ⊥" (vérification de non compatibilité des concepts)
% on ajoute l'intersection dans la A-Box
% (après avoir verifié sa syntaxe et sémentique, et l'avoir mis sous forme atomique et nnf)

acquisition_prop_type2(Abi,Abi1,Tbox) :- 	
			nl, write('Entrez premier concept que vous souhaitez tester :'), nl,
			read(C1), concept(C1), remplace(C1, CA1),
			nl, write('Entrez le concept associé que vous souhaitez tester :'), nl,
			read(C2), concept(C2), remplace(C2, CA2),
			nnf(and(CA1, CA2), NCA),
			genere(Nom),
			concat(Abi, [(Nom, NCA)], Abi1), !.

