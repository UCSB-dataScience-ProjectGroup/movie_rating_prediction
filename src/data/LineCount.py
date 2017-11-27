class LineCount:
    def _make_gen(reader):
        b = reader(1024*1024)
        while b:
            yield b
            b = reader(1024*1024)

    def count(filename):
        f = open(filename, 'rb')
        f_gen = LineCount._make_gen(f.raw.read)
        return sum( buf.count(b'\n') for buf in f_gen )
