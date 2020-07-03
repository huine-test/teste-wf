# -*- coding: utf-8 -*-
class AutomataFunction(object):
    """."""

    def __init__(self, qty_est, states, initial, adjacency, finals):
        """."""
        self.qty_est = qty_est
        self.states = states
        self.initial = initial
        self.adjacency = adjacency
        self.finals = finals

    def _indent(self, text, level=1):
        """."""
        text = text.replace('<sp>', '    ' * level)
        text = text.replace('<spp>', '    ' * (level + 1) )
        return text

    def _make_if(self, array, level=1):
        if not array:
            return ""
        if len(array) == 1:
            item = array.pop()
            nf = self.states[item[1]]

            if isinstance(item[0], int):
                aux = ("<sp>if(tape[index] == %s){\n<spp>index++;\n<spp>" +
                       "%s();\n<sp>}else{\n<spp>REJECT();\n<sp>}")
            else:
                aux = ("<sp>if(tape[index] == '%s'){\n<spp>index++;\n<spp>" +
                       "%s();\n<sp>}else{\n<spp>REJECT();\n<sp>}")

            return self._indent(text=aux, level=level) % (item[0], nf)
        else:
            item = array.pop()
            r = self._make_if(array, (level + 1))
            nf = self.states[item[1]]

            if isinstance(item[0], int):
                aux = ("<sp>if(tape[index] == %s){\n<spp>index++;\n<spp>" +
                       "%s();\n<sp>}else{\n%s\n<sp>}")
            else:
                aux = ("<sp>if(tape[index] == '%s'){\n<spp>index++;\n<spp>" +
                       "%s();\n<sp>}else{\n%s\n<sp>}")

            return self._indent(text=aux, level=level) % (item[0], nf, r)

    def _proto_func(self):
        """."""
        s = []
        for item in range(0, self.qty_est):
            s.append('void %s();' % self.states[item])
        else:
            s.append("")
            s.append("")

        return '\n'.join(s)

    def _main(self):
        """."""
        accept = self._indent(text='void ACCEPT(){\n<sp>cout << "ACCEPT";\n}')
        reject = self._indent(text='void REJECT(){\n<sp>cout << "REJECT";\n}')
        main = self._indent(
            text='int main() {\n<sp>cout << "Input the word: ";\n<sp>' +
            'getline(cin, tape);\n<sp>%s();\n<sp>cin.get();\n' +
            '<sp>return 0;\n}') % self.states[self.initial]

        return '\n'.join(("", accept, "", reject, "", main, ""))

    def _functions(self):
        """."""
        r = []
        base = 'void %s(){\n%s\n}\n'
        for i in range(self.qty_est):
            tmp = [item for item in self.adjacency[i] if item[1] > -1]
            if i in self.finals:
                tmp.append((0, 'accept'))
            r.append(base % (self.states[i], self._make_if(array=tmp)))

        return '\n'.join(r)

    def make(self):
        """."""
        return self._proto_func() + self._main() + self._functions()


class AutomataGoTo(object):
    """."""

    def __init__(self, qty_est, states, initial, adjacency, finals):
        """."""
        self.qty_est = qty_est
        self.states = states
        self.initial = initial
        self.adjacency = adjacency
        self.finals = finals

    def _indent(self, text, level=1):
        """."""
        text = text.replace('<sp>', '    ' * level)
        text = text.replace('<spp>', '    ' * (level + 1))
        return text

    def _make_if(self, array, level=1):
        if not array:
            return ""
        if len(array) == 1:
            item = array.pop()
            nf = self.states[item[1]]

            if isinstance(item[0], int):
                aux = ("<sp>if(tape[index] == %s){\n<spp>index++;\n<spp>" +
                       "goto %s;\n<sp>}else{\n<spp>goto REJECT;\n<sp>}")
            else:
                aux = ("<sp>if(tape[index] == '%s'){\n<spp>index++;\n<spp>" +
                       "goto %s;\n<sp>}else{\n<spp>goto REJECT;\n<sp>}")

            return self._indent(text=aux, level=level) % (item[0], nf)
        else:
            item = array.pop()
            r = self._make_if(array, (level + 1))
            nf = self.states[item[1]]

            if isinstance(item[0], int):
                aux = ("<sp>if(tape[index] == %s){\n<spp>index++;\n<spp>" +
                       "goto %s;\n<sp>}else{\n%s\n<sp>}")
            else:
                aux = ("<sp>if(tape[index] == '%s'){\n<spp>index++;\n<spp>" +
                       "goto %s;\n<sp>}else{\n%s\n<sp>}")

            return self._indent(text=aux, level=level) % (item[0], nf, r)

    def _functions(self):
        """."""
        ret = ["",
               self._indent(text='<sp>ACCEPT:\n<spp>cout << "ACCEPT";\n' +
                            '<spp>goto EXIT;\n'),
               self._indent(text='<sp>REJECT:\n<spp>cout << "REJECT";\n' +
                            '<spp>goto EXIT;\n')]
        base = '    %s:\n%s\n'
        for i in range(self.qty_est):
            tmp = [item for item in self.adjacency[i] if item[1] > -1]
            if i in self.finals:
                tmp.append((0, 'accept'))
            ret.append(base % (self.states[i], self._make_if(array=tmp,
                                                             level=2)))

        return '\n'.join(ret)

    def _main(self):
        """."""
        main = self._indent(
            text='int main() {\n<sp>cout << "Input the word: ";\n<sp>' +
            'getline(cin, tape);\n<sp>goto %s;\n%s\n<sp>EXIT:\n' +
            '<spp>cin.get();\n<spp>return 0;\n}')

        main = main % (self.states[self.initial], self._functions())

        return '\n'.join(("", main, ""))

    def make(self):
        """."""
        return self._main()
