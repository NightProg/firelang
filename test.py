import lexer, unittest, parser, tree

class LexerTest(unittest.TestCase):
    def test_atom(self):
        self.assertTrue(lexer.Atom("a").check())
        self.assertTrue(lexer.Atom("a1").check())
        self.assertTrue(lexer.Atom("a1.2").check())
        self.assertFalse(lexer.Atom("2s").check())
    def test_number(self):
        self.assertTrue(lexer.Number("2").check())
        self.assertFalse(lexer.Number("2s").check())
        self.assertFalse(lexer.Number("2.2s").check())

class ParserTest(unittest.TestCase):
    def test_parse_expr(self):

        tokens = lexer.tokenize("- 2 2")
        self.assertEqual(parser.parse_expr(tokens, tree.Context()), tree.BinOp(tree.Number("2"), lexer.Operator("-"), tree.Number("2")))
        tokens = lexer.tokenize("* 2 3")
        self.assertEqual(parser.parse_expr(tokens, tree.Context()), tree.BinOp(tree.Number("2"),lexer.Operator("*"), tree.Number("3")))
        tokens = lexer.tokenize("/ 5 8 ")
        self.assertEqual(parser.parse_expr(tokens, tree.Context()), tree.BinOp(tree.Number("5"), lexer.Operator("/"), tree.Number("8")))
        tokens = lexer.tokenize("+ 5 5 ")
        self.assertEqual(parser.parse_expr(tokens, tree.Context()).eval(), 10)

unittest.main()