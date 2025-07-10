# Test framework for using kind2-generated test traces to validate a Python
# implementation of a state machine.
#
# Customize to a specific Python target by modifying the CHANGEME lines.

import os
import csv
import Car  # CHANGEME: contains transition functions to test

def get_callable(transfunc):
    parts = transfunc.split('.')
    if len(parts) > 1:
        import sys
        import inspect
        t = sys.modules[parts[0]]
        if len(parts) > 2:
            t = list(filter(lambda e: e[0] == parts[1],
                            inspect.getmembers(t, inspect.isclass)))[0][1]
        return list(filter(lambda e: e[0] == parts[-1],
                           inspect.getmembers(t, inspect.isroutine)))[0][1]
    else:
        return transfunc

def run_test(transfunc, outdir, testname, test_trace):
    # test_trace is a container that will return rows.
    # There is no title row.
    # Each row is varname, vartype, value0, value1, ..., valueN
    # All rows should be the same length
    call = get_callable(transfunc)  #CHANGEME
    outfname = "output_%s" % (testname.split('_')[-1])
    outfpath = os.path.join(outdir, outfname)

    # Consume CSV object to create an internal dict of {inpname: [values]}
    tracedict = {}
    for row in test_trace:
        tracedict[row[0]] = row[2:]

    row0 = list(tracedict.values())[0]
    os.makedirs(outdir, exist_ok=True)

    with open(outfpath, mode='w') as outf:
        for stepnum in range(2, len(row0)):
            stepinps = {i: tracedict[i][stepnum] for i in tracedict}
            r = call(**stepinps)
            outf.write(','.join([str(e) for e in stepinps.values()]))
            outf.write(',')
            outf.write(str(r))
            outf.write('\n')

    print('Wrote', outfpath)


    # tracedict = {}
    # for row in test_trace:
    #     tracedict[row[0], row[1]] = row[2:]
    # sizes = map(lambda (f,t): len(f), tracedict.keys())
    # sizes.append(len('output'))
    # hdrs = map(lambda(s): "%%%ds" % s, sizes)
    # hdr = ' '.intercalate(hdrs)
    # for k in tracedict.keys():
    #     print(k)
    #     print('  =',tracedict[k])


def run_tests(trans_func, in_dir, out_dir):
    files = filter(lambda f: os.path.splitext(f)[1] == '.csv',
                   os.listdir(in_dir))
    files = list(files)
    print('run tests on',files)
    for f in files:
        fname = os.path.join(in_dir, f)
        with open(fname, newline='') as trace_csv:
            run_test(trans_func, out_dir, f, csv.reader(trace_csv))

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        trans_func, inpdir, outdir = sys.argv[1:]
        run_tests(trans_func, inpdir, outdir)
    else:
        usage = lambda s: print(s, file=sys.stderr)
        usage('Usage: %s TRANSITION_FUNCTION INPUT_TRACE_DIR' % sys.argv[0]) # KWQ
        usage('')
        usage('  Calls the TRANSITION_FUNCTION in the Car.py file') # CHANGEME
        usage('  for each test trace .csv file in the INPUT_TRACE_DIR')
        usage('  and writes a transposed .csv file containing the TRANSITION_FUNCTION')
        usage('  output (which can be passed to the kind2-generated rust oracle')
        exit(1)
