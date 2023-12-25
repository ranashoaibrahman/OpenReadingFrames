# Don't change the Libraries
import os
import sys
import re

class ORFFinder:
    def read_fasta_file(self, filepath):
        sequences = {}
        current_header = None
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('>'):
                    if current_header:
                        sequences[current_header] = ''.join(current_sequence)
                    current_header = line[1:]
                    current_sequence = []
                else:
                    current_sequence.append(line)
        if current_header:
            sequences[current_header] = ''.join(current_sequence)
        return sequences

    def find_longest_orf(self, sequence):
        start_codon = 'ATG'
        stop_codons = ['TAA', 'TAG', 'TGA']
        orfs = re.findall(f'{start_codon}(.*?)(?:{"|".join(stop_codons)})', sequence, flags=re.DOTALL)

        longest_orf = ''
        for orf in orfs:
            if len(orf) > len(longest_orf):
                longest_orf = orf

        return longest_orf

    def process_sequences(self, sequences):
        overall_longest_orf = ''
        overall_longest_header = None
        for header, sequence in sequences.items():
            longest_orf = self.find_longest_orf(sequence)
            if longest_orf and len(longest_orf) > len(overall_longest_orf):
                overall_longest_orf = longest_orf
                overall_longest_header = header
        return overall_longest_header, overall_longest_orf
def main():
    if len(sys.argv) < 2:
        print("python orf_finder.py input_file.fasta")
        sys.exit(1)

    file_path = sys.argv[1]

    orf_finder = ORFFinder()
    sequences = orf_finder.read_fasta_file(file_path)
    longest_header, longest_sequence = orf_finder.process_sequences(sequences)

    print(f"Longest DNA sequence found:")
    print(f"Header: {longest_header}")
    print(f"Sequence: {sequences[longest_header]}")
    print(f"Length of the Sequence: {len(sequences[longest_header])}")

if __name__ == "__main__":
    main()
