import re
import os
import sys
       
def memdump_name_generator( output_file ):
	memdump_name_generator.counter += 1
	return "{}memdump{}.mem".format(os.path.splitext(output_file)[0], memdump_name_generator.counter - 1)
memdump_name_generator.counter = 0

def inline_to_dump(input_file, output_file=''):
	ifile = open(input_file, 'r')
	text = ifile.read()
	ifile.close()
	pattern = re.compile(r'  reg \[(.*)\] (\S*) \[(.*)\];\n  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n')

	matches = []
	for match in pattern.finditer(text):
		matches.append(match.group())

	output = text
	output = re.sub(r'  reg \[(.*)\] (\S*) \[(.*)\];\n  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n',
					lambda m: "  reg ["+m.group(1)+"] "+m.group(2)+" [" +m.group(3)+
						"];\n  $readmemh(\""+ memdump_name_generator(output_file) +'", mem);\n', 
					output )

	memdump_name_generator.counter = 0
	for match in matches:
		memdump = ''
		for m in re.finditer(r'\S*\[\S*\] = 8\'h(\S*);\n', match):
			memdump += (m.group(1) +'\n')
		memdump_ofile = open(memdump_name_generator(output_file), 'w')
		memdump_ofile.write(memdump)
		memdump_ofile.close

	if output_file == "":
		output_file = input_file
	ofile = open(output_file, 'w')
	ofile.write(output)
	ofile.close()

if __name__ == '__main__':
	if (len(sys.argv) != 2 and len(sys.argv) != 3):
		print("USAGE: python3 memoryInlineToDump.py <input_file> <output_file>")
	elif len(sys.argv) == 2:
		inline_to_dump(sys.argv[1])
	else: #len == 3
		inline_to_dump(sys.argv[1],sys.argv[2])
	