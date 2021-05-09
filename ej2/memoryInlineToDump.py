import re
import os

def inline_to_dump(input_file, output_file):
	output_name = os.path.splitext(output_file)[0]
	ifile = open(input_file, 'r')
	text = ifile.read()
	ifile.close()
	pattern = re.compile(r'  reg \[(.*)\] (\S*) \[(.*)\];\n  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n')

	matches = []
	for match in pattern.finditer(text):
		matches.append(match.group())

	i = 0
	output = text
	for match in matches:
		output = re.sub(	r'  reg \[(.*)\] (\S*) \[(.*)\];\n  initial begin\n((    \S*\[\S*\] = \S*;\n)*)  end\n',
					r'  reg [\1] \2 [\3];\n  $readmemh("'+ 
					output_name + 'memdump' + str(i)+ '.mem", mem);\n', output, 1 )
		
		memdump = ''
		for m in re.finditer(r'\S*\[\S*\] = 8\'h(\S*);\n', match):
			memdump += (m.group(1) +'\n')
		
		memdump_ofile = open(output_name + 'memdump' + str(i)+ '.mem', 'w')
		memdump_ofile.write(memdump)
		memdump_ofile.close
			
		i += 1

	ofile = open(output_file, 'w')
	ofile.write(output)
	ofile.close()


if __name__ == '__main__':
	inline_to_dump('testcase.v','xd.v')