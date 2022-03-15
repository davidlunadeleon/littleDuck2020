grammar LittleDuck2020;

// Language reserved keywords
ELSE 	: 'myelse' ;
IF		: 'if' ;
PRINT	: 'print' ;
PROGRAM : 'program' ;
T_FLOAT	: 'float' ;
T_INT	: 'int' ;
VAR		: 'var' ;

// Lexer rules
fragment DIGIT 		: [0-9] ;
ASSIGN	: '=' ;
COMPOP	: ('<>'|'<'|'>') ;
EXPOP	: [+-] ;
FLOAT	: DIGIT+ '.' DIGIT+ ;
ID		: [a-zA-Z][a-zA-Z0-9_]* ;
INT		: DIGIT+ ;
LITERAL	: '"' .*? '"' ;
TERMOP	: [*/] ;
WS		: [ \t] -> skip;

// Parser rules
p	: pprime1 myvars block
	| pprime1 block
	;

pprime1	: PROGRAM ID ';' ;

myvars	: VAR varlists ;

varlists	: varlistsprime1 varlists
			| varlistsprime1
			;

varlistsprime1	: idlist ':' mytype ';' ;

idlist	: ID ',' idlist
		| ID
		;

block	: '{' statements '}' ;

statements	: statement statements
			| // empty
			;

statement	: assignment
			| conditional
			| writing
			;

assignment	: ID ASSIGN expression ';' ;

exp	: term EXPOP exp
	| term
	;

expression	: exp COMPOP exp
			| exp
			;

term	: factor TERMOP term 
		| factor
		;

mytype	: T_FLOAT
		| T_INT
		;

varcte	: FLOAT
		| ID
		| INT
		;

conditional	: IF '(' expression ')' block myelse ';' ;

myelse	: myelse block
		| // empty
		;

factor	: '(' expression ')'
		| TERMOP varcte
		| varcte
		;

writing	: PRINT '(' writinglist ')' ';' ;

writinglist	: expression ',' writinglist
			| LITERAL ',' writinglist
			| expression
			| LITERAL
			;
