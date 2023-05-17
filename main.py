import numpy
import pyperclip


def make_stuff(values):
    def print_desmos(coe: numpy.ndarray):
        total = ""
        for i in range(len(coe)):
            total += str(abs(coe[i])) + 'x^' + "{(" + str(len(coe) - i - 1) + ")}"
            next_item = i + 1
            if len(coe) > next_item:
                if coe[next_item] > 0:
                    total += "+"
                else:
                    total += "-"
        while 'e' in total:
            start = total.find('e')
            for i in range(start, len(total)):
                if total[i] == 'x':
                    total = total[0:start] + "*10^{(" + total[start + 1:i] + ")}" + total[i:]
                    break
        if coe[0] < 0:
            total = '-' + total
        pyperclip.copy(total + '\\left\\{' + f'{numpy.min(x)} <= x <= {numpy.max(x)}' + '\\right\\}')

    x = numpy.zeros(len(values))
    y = numpy.zeros(len(values))
    for i in range(len(values)):
        xval, yval = values[i]
        x[i] = xval
        y[i] = yval

    mat = numpy.vander(x, 9)
    vals = numpy.linalg.lstsq(mat, y, None)[0]
    print_desmos(vals)
