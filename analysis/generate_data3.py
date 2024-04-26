def generate_data(start_attr, end_attr, output_file):
    with open('input4.txt', 'w') as file:
        for n in range(start_attr, end_attr + 1):
            attributes_line = ' '.join(f'attr_{i}' for i in range(1, n + 1))
            file.write(f'sahaj\n{attributes_line}\n')
            
            delhi_line = 'delhi'
            file.write(f'{delhi_line}\n')
            
            and_line = ' and '.join(f'attr_{i}' for i in range(1, n + 1))
            file.write(f'{and_line}\n')
            
            delhi_mumbai_line = 'delhi,mumbai'
            file.write(f'{delhi_mumbai_line}\n')
            
            hi_line = 'hi'
            file.write(f'{hi_line}\n\n')  # Add a blank line for separation

start_attr = 2
end_attr = 3
output_file = 'output.txt'
generate_data(start_attr, end_attr, output_file)
