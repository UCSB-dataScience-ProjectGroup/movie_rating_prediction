class LineCount:
    @staticmethod
    def _make_gen(reader):
        b = reader(1024*1024)
        while b:
            yield b
            b = reader(1024*1024)

    @staticmethod
    def count(filename):
        f = open(filename, 'rb')
        f_gen = LineCount._make_gen(f.read)
        return sum( buf.count(b'\n') for buf in f_gen )
