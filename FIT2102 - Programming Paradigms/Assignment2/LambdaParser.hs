module LambdaParser where

import Parser
import Data.Lambda
import Data.Builder

data Expr = E {op :: Builder, value :: Builder}

-- You can add more imports if you need them

-- Remember that you can (and should) define your own functions, types, and
-- parser combinators. Each of the implementations for the functions below
-- should be fairly short and concise.

open :: Parser Char
open = is '('

close :: Parser Char
close = is ')'

lambdaChar :: Parser Char
lambdaChar = is 'λ' ||| is '/'

dotChar :: Parser Char
dotChar = is '.'

char :: Parser Char
char = oneof "abcdefghijklmnopqrstuvwxyz"

{-|
    Part 1
-}

-- | Exercise 1

-- | Parses a string representing a lambda calculus expression in long form
--
-- <longLambdaP> ::= <input> <output> | <input> <longLambdaP> <close>
-- <input> ::= <open> <lambdaChar> <char> <dotChar>
-- <output> ::= <nextChar> <argl> <close> | <nextChar> <close>
-- <argl> ::= <open> <nextChar> <close>
-- <nextChar> ::= <char> <nextChar> | <char>
-- <open> ::= "("
-- <close> ::= ")"
-- <lambdaChar> ::= "λ" | "/"
-- <dotChar> ::= "."
-- <char> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"


input :: Parser Char
input = open >> lambdaChar >> char <* dotChar

output :: Parser Builder
output = (do
    a <- nextChar
    b <- argl
    close
    return (a `ap` b)) |||
    (do
    a <- nextChar
    close
    pure a)

argl :: Parser Builder
argl = between open close nextChar

nextChar :: Parser Builder
nextChar = (do
    a <- char
    b <- nextChar
    return $ term a `ap` b) |||
    (term <$> char)

-- >>> parse longLambdaP "(λx.xx)"
-- Result >< \x.xx
--
-- >>> parse longLambdaP "(λx.(λy.xy(xx)))"
-- Result >< \xy.xy(xx)
--
-- >>> parse longLambdaP "(λx(λy.x))"
-- UnexpectedChar '('
--

longLambdaP :: Parser Lambda
longLambdaP = build <$> longLambdaPAux

longLambdaPAux :: Parser Builder
longLambdaPAux = (do
    a <- input
    b <- output
    return (lam a b)) |||
    (do
    a <- input
    b <- longLambdaPAux
    close
    return (lam a b))


-- | Parses a string representing a lambda calculus expression in short form
--
-- <shortLambdaP> ::= <open> <inp> <outp> <close> | <open> <inp> <outp> <close> <shortLambdaP> | <inp> <outp>
-- <inp> ::= <lambdaChar> <nextChar> 
-- <outp> ::= <dotChar> <nextChar> | <dotChar> <args>
-- <args> ::= <nextChar> <open> <nextChar> <close> | <nextChar> <shortLambdaP>
-- <nextChar> ::= <char> <nextChar> | <char>
-- <open> ::= "("
-- <close> ::= ")"
-- <lambdaChar> ::= "/"
-- <dotChar> ::= "."
-- <char> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"

-- >>> parse shortLambdaP "λx.xx"
-- Result >< \x.xx
--
-- >>> parse shortLambdaP "λxy.xy(xx)"
-- Result >< \xy.xy(xx)
--
-- >>> parse shortLambdaP "λx.x(λy.yy)"
-- Result >< \x.x\y.yy
--
-- >>> parse shortLambdaP "(λx.x)(λy.yy)"
-- Result >< (\x.x)\y.yy
--
-- >>> parse shortLambdaP "λxyz"
-- UnexpectedEof

nextChari :: Parser [Char]
nextChari = list char

inp :: Parser [Char]
inp = lambdaChar >> nextChari

outp :: Parser Builder
outp = (dotChar >> args) ||| (dotChar >> nextChar)

args :: Parser Builder
args = (do
    a <- nextChar
    b <- between open close nextChar
    return (a `ap` b)) |||
    (do
    a <- nextChar
    b <- shortLambdaAux
    return (a `ap` b))

shortLambdaP :: Parser Lambda
shortLambdaP = do
    a <- shortLambdaAux
    b <- list shortLambdaAux
    return $ build $ foldl ap a b

shortLambdaAux :: Parser Builder
shortLambdaAux = (do
    open
    a <- inp
    b <- outp
    close
    return $ foldr lam b a) |||
    (do
    open
    a <- inp
    b <- outp
    close
    c <- shortLambdaAux
    return $ foldr lam (b `ap` c) a) |||
    (do
    a <- inp
    b <- outp
    return $ foldr lam b a)

-- | Parses a string representing a lambda calculus expression in short or long form
--
-- <lambdaP> ::= <longLambdaP> | <shortLambdaP>
-- >>> parse lambdaP "λx.xx"
-- Result >< \x.xx
--
-- >>> parse lambdaP "(λx.xx)"
-- Result >< \x.xx
--
-- >>> parse lambdaP "λx..x"
-- UnexpectedChar '.'
lambdaP :: Parser Lambda
lambdaP = longLambdaP ||| shortLambdaP 

{-|
    Part 2
-}

-- | Exercise 1
-- parser for the "True" keyword
true :: Parser Builder
true = tok $ string "True" >> return (boolToLam True)
--parser for the "False" keyword
false :: Parser Builder
false = tok $ string "False" >> return (boolToLam False)
--church encoding for IF
ifB :: Builder
ifB = lam 'b' $ lam 't' $ lam 'f' $ term 'b' `ap` term 't' `ap` term 'f'
--church encoding for AND
andB :: Builder
andB = lam 'x' $ lam 'y' $ ifB `ap` term 'x' `ap` term 'y' `ap` boolToLam False
--church encoding for OR
orB :: Builder
orB = lam 'x' $ lam 'y' $ ifB `ap` term 'x' `ap` boolToLam True `ap` term 'y'
--church encoding for NOT
notB :: Builder
notB = lam 'x' $ ifB `ap` term 'x' `ap` boolToLam False `ap` boolToLam True
--general parser for booleans, in the order of NOT > IF > AND > OR > T/F
boolean :: Parser Builder
boolean = notP ||| ifP ||| andP ||| orP ||| true ||| false
--parser for parsing either bracketed input or non-bracketed input
bracketed :: Parser Builder -> Parser Builder
bracketed p = p ||| between open close p
--parser for the "not" keyword in input
notP :: Parser Builder
notP = do
    tok $ string "not"
    a <- bracketed boolean
    return $ notB `ap` a
--parser for the "and" keyword in input
andP :: Parser Builder
andP = do
    tok $ string "and"
    a <- bracketed boolean
    return $ andB `ap` a
--parser for the "or" keyword in input
orP :: Parser Builder
orP = do
    tok $ string "or"
    a <- bracketed boolean
    return $ orB `ap` a
-- general parser for parsing arithmetic/logic expressions, takes in an input parser which either parses arithmetic/logic
expr :: Parser Builder -> Parser Builder
expr p = do
    a1 <- bracketed p
    a2 <- list $ bracketed p
    return $ foldl (flip ap) a1 a2
--parser for the "if...then...else" keyword in input
ifP :: Parser Builder
ifP = do
    tok $ string "if"
    a <- expr boolean
    tok $ string "then"
    b <- expr boolean
    tok $ string "else"
    c <- expr boolean
    return $ ifB `ap` a `ap` b `ap` c

-- IMPORTANT: The church encoding for boolean constructs can be found here -> https://tgdwyer.github.io/lambdacalculus/#church-encodings

-- | Parse a logical expression and returns in lambda calculus
-- >>> lamToBool <$> parse logicP "True and False"
-- Result >< Just False
--
-- >>> lamToBool <$> parse logicP "True and False or not False and True"
-- Result >< Just True
--
-- >>> lamToBool <$> parse logicP "not not not False"
-- Result >< Just True
--
-- >>> parse logicP "True and False"
-- Result >< (\xy.(\btf.btf)xy\_f.f)(\t_.t)\_f.f
--
-- >>> parse logicP "not False"
-- Result >< (\x.(\btf.btf)x(\_f.f)\t_.t)\_f.f
-- >>> lamToBool <$> parse logicP "if True and not False then True or True else False"
-- Result >< Just True
logicP :: Parser Lambda
logicP = do
    a <- expr boolean
    return $ build a

-- | Exercise 2

-- Code from week11 tutorial Parser.hs
tok :: Parser a -> Parser a
tok = flip (<*) (list space)

-- Code from week11 tutorial Instances.hs
readInt :: String -> Maybe (Int, String)
readInt s = case reads s of
  [(x, rest)] -> Just (x, rest)
  _           -> Nothing

-- Code from week11 tutorial Parser.hs
int :: Parser Int
int = P f
 where
  f "" = Error UnexpectedEof
  f x  = case readInt x of
    Just (v, rest) -> Result rest v
    Nothing        -> Error $ UnexpectedChar (head x)
--parses an integer in the input
number :: Parser Builder
number = do
    a <- tok int
    return $ intToLam a
--parser for basic arithmetic operators (+ and -)
basicOperator :: Parser Expr
basicOperator = do
    a <- addP ||| minusP
    b <- number
    return $ E a b
--lambda church encoding for SUCC
succB :: Builder
succB = lam 'n' $ lam 'f' $ lam 'x' $ term 'f' `ap` (term 'n' `ap` term 'f' `ap` term 'x')
--lambda church encoding for PRED
predB :: Builder
predB = lam 'n' $ lam 'f' $ lam 'x' $ term 'n' `ap` (lam 'g' $ lam 'h' $ term 'h' `ap` (term 'g' `ap` term 'f')) `ap` (lam 'u' $ term 'x') `ap` (lam 'u' $ term 'u')
--lambda church encoding for ADD
addB :: Builder
addB = lam 'x' $ lam 'y' $ term 'y' `ap` succB `ap` term 'x'
--lambda church encoding for MINUS
minusB :: Builder
minusB = lam 'x' $ lam 'y' $ term 'y' `ap` predB `ap` term 'x'
--parser for the "+" keyword in input
addP :: Parser Builder
addP = tok $ is '+' >> return addB
--parser for the "-" keyword in input
minusP :: Parser Builder
minusP = tok $ is '-' >> return minusB

-- | The church encoding for arithmetic operations are given below (with x and y being church numerals)

-- | x + y = add = λxy.y succ x
-- | x - y = minus = λxy.y pred x
-- | x * y = multiply = λxyf.x(yf)
-- | x ** y = exp = λxy.yx

-- | The helper functions you'll need are:
-- | succ = λnfx.f(nfx)
-- | pred = λnfx.n(λgh.h(gf))(λu.x)(λu.u)
-- | Note since we haven't encoded negative numbers pred 0 == 0, and m - n (where n > m) = 0

-- | Parse simple arithmetic expressions involving + - and natural numbers into lambda calculus
-- >>> lamToInt <$> parse basicArithmeticP "5 + 4"
-- Result >< Just 9
--
-- >>> lamToInt <$> parse basicArithmeticP "5 + 9 - 3 + 2"
-- Result >< Just 13
basicArithmeticP :: Parser Lambda
basicArithmeticP = do
    a <- number
    b <- list basicOperator

    return $ build $ foldl (\acc x -> op x `ap` acc `ap` value x) a b

--helper parser for parsing basic arithmetic operations, returns type Builder instead of Lambda
basicP :: Parser Builder
basicP = do
    a <- number
    b <- list basicOperator

    return $ foldl (\acc x -> op x `ap` acc `ap` value x) a b
--parser for arithmetic operators (+, -, * and **)
operator :: Parser Expr
operator = do
    a <- addP ||| minusP
    b <- expP ||| multiplyP ||| number
    return $ E a b
--lambda church encoding for MULTIPLY
multiplyB :: Builder
multiplyB = lam 'x' $ lam 'y' $ lam 'f' $ term 'x' `ap` (term 'y' `ap` term 'f')
--lambda church encoding for EXP
expB :: Builder
expB = lam 'x' $ lam 'y' $ term 'y' `ap` term 'x'
--parser for the "*" keyword in input
multiplyP :: Parser Builder
multiplyP = do
    a <- number
    is '*'
    b <- expP ||| number
    return $ multiplyB `ap` a `ap` b
--parser for the "**" keyword in input
expP :: Parser Builder
expP = do
    a <- number
    string "**"
    b <- between open close basicP ||| number
    return $ expB `ap` a `ap` b

-- | Parse arithmetic expressions involving + - * ** () and natural numbers into lambda calculus
-- >>> lamToInt <$> parse arithmeticP "5 + 9 * 3 - 2**3"
-- Result >< Just 24
--
-- >>> lamToInt <$> parse arithmeticP "100 - 4 * 2**(4-1)"
-- Result >< Just 68
arithmeticP :: Parser Lambda
arithmeticP = do
    a <- expP ||| multiplyP ||| between open close basicP ||| number
    b <- list operator
    return $ build $ foldl (\acc x -> op x `ap` acc `ap` value x) a b


-- | Exercise 3
-- lambda church encoding for LEQ
leqB :: Builder
leqB = lam 'm' $ lam 'n' $ isZero  `ap` (minusB `ap` term 'm' `ap` term 'n')
-- lambda church encoding for LT
-- adapted from https://stackoverflow.com/questions/20523625/looking-for-a-church-encoding-lambda-calculus-to-define#:~:text=Lesser%20than%20(%20LT%20or%20%3C%20),).
lessThanB :: Builder
lessThanB = lam 'x' $ lam 'y' $ greaterThanB `ap` term 'y' `ap` term 'x'
-- lambda church encoding for GT
-- adapted from https://stackoverflow.com/questions/20523625/looking-for-a-church-encoding-lambda-calculus-to-define#:~:text=Lesser%20than%20(%20LT%20or%20%3C%20),).
greaterThanB :: Builder
greaterThanB = lam 'x' $ lam 'y' $ notB `ap` (isZero `ap` (minusB `ap` term 'x' `ap` term 'y'))
-- lambda church encoding for integer ==
eqB :: Builder
eqB = lam 'm' $ lam 'n' $ andB `ap` (leqB `ap` term 'm' `ap` term 'n') `ap` (leqB `ap` term 'n' `ap` term 'm')
-- lambda church encoding for isZero
isZero :: Builder
isZero = lam 'n' $ term 'n' `ap` (lam 'x' $ boolToLam False) `ap` boolToLam True
-- parser for the "<=" keyword
leqP :: Parser Builder
leqP = do
    a <- arithmeticP
    tok $ string "<="
    b <- arithmeticP
    return $ (build $ (build $ leqB) `ap'` a) `ap'` b
-- parser for the "<" keyword
lessThanP :: Parser Builder
lessThanP = do
    a <- arithmeticP
    tok $ string "<"
    b <- arithmeticP
    return $ (build $ (build $ lessThanB) `ap'` a) `ap'` b
-- parser for the ">" keyword
greaterThanP :: Parser Builder
greaterThanP = do
    a <- arithmeticP
    tok $ string ">"
    b <- arithmeticP
    return $ (build $ (build $ greaterThanB) `ap'` a) `ap'` b
-- parser for the "==" keyword for integers
eqP :: Parser Builder
eqP = do
    a <- arithmeticP 
    tok $ string "=="
    b <- arithmeticP 
    return $ (build $ (build $ eqB) `ap'` a) `ap'` b
-- parser for the "!=" keyword
noteqP :: Parser Builder
noteqP = do
    a <- arithmeticP
    tok $ string "!="
    b <- arithmeticP
    return $ notB `ap` ((build $ (build $ eqB) `ap'` a) `ap'` b)
-- lambda church encoding for XOR
xor :: Builder
xor = lam 'p' $ lam 'q' $ term 'p' `ap` (term 'q' `ap` boolToLam False `ap` boolToLam True) `ap` term 'q' 
-- lambda church encoding for boolean ==
eqBoolB :: Builder
eqBoolB = lam 'p' $ lam 'q' $ notB `ap` (xor `ap` term 'p' `ap` term 'q')
-- parses the "==" keyword for comparing booleans
eqBoolP :: Parser Builder
eqBoolP = do
    a <- logicP
    tok $ string "=="
    b <- logicP
    return $ (build $ (build $ eqBoolB) `ap'` a) `ap'` b
-- supports comparison of <=, <, >, ==, !=
complexBoolean :: Parser Builder
complexBoolean = leqP ||| lessThanP ||| greaterThanP ||| eqP ||| noteqP ||| eqBoolP
-- parser for the "not" keyword of complex logic expressions
complexNotP :: Parser Builder
complexNotP = do
    tok $ string "not"
    a <- complexBoolean
    return $ notB `ap` a
-- parser for the "and" keyword of complex logic expressions
complexAndP :: Parser Builder
complexAndP = do
    tok $ string "and"
    a <- complexBoolean
    return $ andB `ap` a
-- parser for the "or" keyword of complex logic expressions
complexOrP :: Parser Builder
complexOrP =  do
    tok $ string "or"
    a <- complexBoolean
    return $ orB `ap` a
-- parser for the "if...then...else" keyword of complex logic expressions
complexIfP :: Parser Builder
complexIfP = do
    tok $ string "if"
    a <- expr complexBoolean
    tok $ string "then"
    b <- expr complexBoolean
    tok $ string "else"
    c <- expr complexBoolean
    return (a `ap` b `ap` c)


-- | The church encoding for comparison operations are given below (with x and y being church numerals)

-- | x <= y = LEQ = λmn.isZero (minus m n)
-- | x == y = EQ = λmn.and (LEQ m n) (LEQ n m)

-- The church encoding for comparison of booleans, adapted from https://stackoverflow.com/questions/21010258/how-to-implement-eq-of-lisp-in-lambda-calculus
-- xor = λ p q. p (q F T) q
-- equ = λ p q. not (xor p q)

-- | The helper function you'll need is:
-- | isZero = λn.n(λx.False)True

-- >>> lamToBool <$> parse complexCalcP "9 - 2 <= 3 + 6"
-- Result >< Just True
--
-- >>> lamToBool <$> parse complexCalcP "15 - 2 * 2 != 2**3 + 3 or 5 * 3 + 1 < 9"
-- Result >< Just False
complexCalcP :: Parser Lambda
complexCalcP = do
    a <- complexBoolean
    b <- list $ complexNotP ||| complexIfP ||| complexAndP ||| complexOrP ||| complexBoolean
    return $ build $ foldl (flip ap) a b


{-|
    Part 3
-}

-- | Exercise 1
-- lambda church encoding for a null (empty) list
nullL :: Lambda
nullL = build $ lam 'c' $ lam 'n' $ term 'n'
-- lambda church encoding for the cons function
consL :: Lambda
consL = build $ lam 'h' $ lam 't' $ lam 'c' $ lam 'n' $ term 'c' `ap` term 'h' `ap` (term 't' `ap` term 'c' `ap` term 'n')
-- parser for a null list
nullP :: Parser Lambda
nullP = do
    is '['
    is ']'
    return nullL

-- | The church encoding for list constructs are given below
-- | [] = null = λcn.n
-- | isNull = λl.l(λht.False) True
-- | cons = λhtcn.ch(tcn)
-- | head = λl.l(λht.h) False
-- | tail = λlcn.l(λhtg.gh(tc))(λt.n)(λht.t)
--
-- >>> parse listP "[]"
-- Result >< \cn.n
--
-- >>> parse listP "[True]"
-- Result >< (\htcn.ch(tcn))(\t_.t)\cn.n
--
-- >>> parse listP "[0, 0]"
-- Result >< (\htcn.ch(tcn))(\fx.x)((\htcn.ch(tcn))(\fx.x)\cn.n)
--
-- >>> parse listP "[0, 0"
-- UnexpectedEof
listP :: Parser Lambda
listP = nullP
    ||| (do
        a <- between (is '[') (is ']') (arithmeticP ||| logicP)
        return $ build $ ap' (build $ ap' consL a) nullL)
    ||| (do
    is '['
    a <- (arithmeticP ||| logicP) <* tok (is ',')
    b <- list $ (arithmeticP ||| logicP) <* tok (is ',')
    c <- arithmeticP ||| logicP
    is ']'
    return $ build $ ap' (build $ ap' consL a) (foldr (\x acc  -> build $ ap' (build $ ap' consL x) acc) (build $ ap' (build $ ap' consL c) nullL) b ))

-- lambda church encoding for isNull
isNullL :: Lambda
isNullL = build $ lam 'l' $ term 'l' `ap` (lam 'h' $ lam 't' $ boolToLam False) `ap` boolToLam True
-- lambda church encoding for head
headL :: Lambda
headL = build $ lam 'l' $ term 'l' `ap` (lam 'h' $ lam 't' $ term 'h') `ap` boolToLam False
-- lambda church encoding for tail/rest
tailL :: Lambda
tailL = build $ lam 'l' $ lam 'c' $ lam 'n' $ term 'l' `ap` (lam 'h' $ lam 't' $ lam 'g' $ term 'g' `ap` term 'h' `ap` (term 't' `ap` term 'c')) `ap` (lam 't' $ term 'n') `ap` (lam 'h' $ lam 't' $ term 't')
-- parser for the "isNull" keyword
isNullP :: Parser Lambda
isNullP = tok $ string "isNull" >> return isNullL
-- parser for the "head" keyword
headP :: Parser Lambda
headP = tok $ string "head" >> return headL
-- parser for the "rest" keyword
tailP :: Parser Lambda
tailP = tok $ string "rest" >> return tailL

-- >>> lamToBool <$> parse listOpP "head [True, False, True, False, False]"
-- Result >< Just True
--
-- >>> lamToBool <$> parse listOpP "head rest [True, False, True, False, False]"
-- Result >< Just False
--
-- >>> lamToBool <$> parse listOpP "isNull []"
-- Result >< Just True
--
-- >>> lamToBool <$> parse listOpP "isNull [1, 2, 3]"
-- Result >< Just False
listOpP :: Parser Lambda
listOpP = do
    a <- list $ isNullP ||| headP ||| tailP
    b <- listP
    return $ foldr (\x acc -> build $ ap' x acc) b a


-- | Exercise 2
-- lambda church encoding for the U combinator
builderU :: Builder
builderU = lam 'f' $ term 'f' `ap` term 'f'
-- lambda church encoding for the factorial function
factB :: Builder
factB = builderU `ap` (lam 'f' $ lam 'n' $ isZero `ap` term 'n' `ap` intToLam 1 `ap` (multiplyB `ap` term 'n' `ap` (term 'f' `ap` term 'f' `ap` (predB `ap` term 'n'))))

-- Implement your function(s) of choice below!
--
-- | Factorial parser using the U combinator
-- church encoding adapted from https://stackoverflow.com/questions/46820404/non-recursive-lambda-calculus-factorial-function?fbclid=IwAR24vsp82d2F9cS55apfuA2OgA0xT3WMg6PxSrcqsjYyA6P6HPljahV1OSw
factP :: Parser Lambda
factP = do
    a <- number
    tok $ is '!'
    return $ build $ factB `ap` a

-- | Parser for the map function
-- map f l = if l isNull then null else map f (cons (f head l) (rest l))
isNullB :: Builder
isNullB = lam 'l' $ term 'l' `ap` (lam 'h' $ lam 't' $ boolToLam False) `ap` boolToLam True

nullB :: Builder
nullB = lam 'c' $ lam 'n' $ term 'n'

headB :: Builder
headB = lam 'l' $ term 'l' `ap` (lam 'h' $ lam 't' $ term 'h') `ap` boolToLam False

tailB :: Builder
tailB = lam 'l' $ lam 'c' $ lam 'n' $ term 'l' `ap` (lam 'h' $ lam 't' $ lam 'g' $ term 'g' `ap` term 'h' `ap` (term 't' `ap` term 'c')) `ap` (lam 't' $ term 'n') `ap` (lam 'h' $ lam 't' $ term 't')

consB :: Builder
consB = lam 'h' $ lam 't' $ lam 'c' $ lam 'n' $ term 'c' `ap` term 'h' `ap` (term 't' `ap` term 'c' `ap` term 'n')

mapB :: Builder
mapB = builderU `ap` (lam 'g' $ lam 'f' $ lam 'l' $ ifB `ap` term 'l' `ap` isNullB `ap` nullB `ap` (term 'g' `ap` term 'g' `ap` term 'f' `ap` (consB `ap` (term 'f' `ap` (headB `ap` term 'l')) `ap` (tailB `ap` term 'l'))))

mapP :: Parser Lambda
mapP = do
    tok $ string "map"
    op <- addP ||| minusP
    n <- number
    l <- listP
    return $ build $ ap' (build (mapB `ap` (op `ap` n))) l


-- | Parser for the quicksort algorithm
-- church encoding adapted from https://www.quora.com/How-can-a-Quick-Sort-algorithm-be-implemented-in-Lambda-Calculus?fbclid=IwAR2T0VRZKXCn6wfcmv1hzuRA0LZZlBS_OcI_gN37wIYb63CJbgF0Hh6KA5c
-- Y      = λf.(λx.f (x x))(λx.f (x x)) 
-- Id     = λx.x 
-- Flip   = λf.λx.λy.f y x 
 
-- True   = λt.λf.t 
-- False  = λt.λf.f 
-- Not    = λb.b False True 
 
-- Zero   = λf.λx.x 
-- Succ   = λn.λf.λx.f (n f x) 
 
-- Pred   = λn.λf.λx.n (λg.λh.h (g f)) (λc.x) Id 
-- Minus  = λm.λn.(n Pred) m 
-- IsZero = λn.n (λf.False) True 
-- LessEq = λm.λn.IsZero (Minus m n) 
-- Greatr = λm.λn.Not (LessEq m n) 
 
-- Nil    = λx.λc.x 
-- Cons   = λh.λt.λx.λc.c h t 
 
-- FLCat  = λf.λx.λy.x y (λh.λt.Cons h (f t y)) 
-- LCat   = Y FLCat 
 
-- FFlter = λf.λp.λl.l Nil (λh.λt.((p h) (Cons h) Id) (f p t)) 
-- Filter = Y FFlter 
 
-- FQSort = λf.λl.l Nil  
--                  (λh.λt.LCat (f (Filter ((Flip LessEq) h) t))  
--                               (Cons h (f (Filter ((Flip Greatr) h) t)))) 
-- QSort  = Y FQSort 
builderY :: Builder
builderY = lam 'f' $ (lam 'x' $ term 'f' `ap` (term 'x' `ap` term 'x')) `ap` (lam 'x' $ term 'f' `ap` (term 'x' `ap` term 'x'))

idB :: Builder
idB = lam 'x' $ term 'x'

flipB :: Builder
flipB = lam 'f' $ lam 'x' $ lam 'y' $ term 'f' `ap` term 'y' `ap` term 'x'

fnot :: Builder
fnot = lam 'b' $ term 'b' `ap` boolToLam False `ap` boolToLam True

predes :: Builder
predes = lam 'n' $ lam 'f' $ lam 'x' $ term 'n' `ap` (lam 'g' $ lam 'h' $ term 'h' `ap` (term 'g' `ap` term 'f')) `ap` (lam 'c' $ term 'x') `ap` idB

minus :: Builder
minus = lam 'm' $ lam 'n' $ (term 'n' `ap` predes) `ap` term 'm'

lesseq :: Builder
lesseq = lam 'm' $ lam 'n' $ isZero `ap` (minus `ap` term 'm' `ap` term 'n')

greatr :: Builder
greatr = lam 'm' $ lam 'n' $ fnot `ap` (lesseq `ap` term 'm' `ap` term 'n')

flcat :: Builder
flcat = lam 'f' $ lam 'x' $ lam 'y' $ term 'x' `ap` term 'y' `ap` (lam 'h' $ lam 't' $ consB `ap` term 'h' `ap` (term 'f' `ap` term 't' `ap` term 'y')) 

lcat :: Builder 
lcat = builderY `ap` flcat

ffilter :: Builder
ffilter = lam 'f' $ lam 'p' $ lam 'l' $ term 'l' `ap` nullB `ap` (lam 'h' $ lam 't' $ ((term 'p' `ap` term 'h') `ap` (consB `ap` term 'h') `ap` idB) `ap` (term 'f' `ap` term 'p' `ap` term 't'))

filterB :: Builder
filterB = builderY `ap` ffilter

fqsort :: Builder
fqsort = lam 'f' $ lam 'l' $ term 'l' `ap` nullB `ap` (lam 'h' $ lam 't' $ lcat `ap` (term 'f' `ap` (filterB `ap` ((flipB `ap` lesseq) `ap` term 'h') `ap` term 't')) `ap` (consB `ap` term 'h' `ap` (term 'f' `ap` (filterB `ap` ((flipB `ap` greatr) `ap` term 'h') `ap` term 't'))))

quicksortB :: Lambda
quicksortB = build $ builderY `ap` fqsort

quicksortP :: Parser Lambda
quicksortP = do
    tok $ string "quicksort"
    l <- listP
    return $ build $ ap' quicksortB l
