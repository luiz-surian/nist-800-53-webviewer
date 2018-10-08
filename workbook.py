__author__ = 'Luiz Fernando Surian Filho'

import json
import time

import xlsxwriter

file_path = './bin/files/nist/'


def _xhtml_parser(key, value):
    output = ''
    if key == 'ns2:p':
        if type(value) is dict:
            holder = f'{value["#text"]} \n'
            if 'ns2:em' in value:
                holder = holder.replace('[]', f'[{value["ns2:em"]}]')
        else:
            holder = ''
            for v in value:
                holder += f'{v["#text"]} \n'
                if 'ns2:em' in value:
                    holder = holder.replace('[]', f'[{v["ns2:em"]}]')

        output += holder

    elif key == 'ns2:ol':
        for item in value['ns2:li']:
            if type(item) is not str:
                holder = f'{item} \n'
                if 'ns2:em' in item:
                    if type(item['ns2:em']) is not str:
                        for em in item['ns2:em']:
                            holder = holder.replace('[]', f'[{em}]')
                    else:
                        holder = holder.replace('[]', f'[{item["ns2:em"]}]')

                output += holder
            else:
                output += f'{item} \n'

    else:
        output += f'ERROR - couldn\'t parse key: [{key}] \n'

    return output


def write(content):

    timestamp = int(time.time())
    file_name = f'nist800_53_{timestamp}.xlsx'
    workbook = xlsxwriter.Workbook(f'bin/{file_name}')
    worksheet = workbook.add_worksheet('NIST 800-53')

    worksheet.set_column('A:A', 50)
    worksheet.set_column('B:B', 80)
    worksheet.set_column('C:C', 80)
    worksheet.set_column('D:D', 80)
    worksheet.set_column('E:E', 80)

    normal = workbook.add_format({
        'text_wrap': 1,
        'valign': 'top',
    })

    bold = workbook.add_format({
        'text_wrap': 1,
        'valign': 'top',
        'bold': True,
    })

    worksheet.write('A1', 'NIST 800-53', bold)
    worksheet.write('B1', 'Description', bold)
    worksheet.write('C1', 'Supplemental Guidance', bold)
    worksheet.write('D1', 'References', bold)
    worksheet.write('E1', 'Control Enhancements', bold)

    i = 2
    listing = json.loads(content['listing'][0])
    for key, value in listing.items():
        worksheet.write(f'A{i}', value, normal)
        with open(f'{file_path}{key}.json') as json_data:
            vulnerability = json.load(json_data)

            # Description
            output = ''
            if 'description' in vulnerability:
                desc = vulnerability['description']['ns2:div']
                for item in desc:
                    output += _xhtml_parser(item, desc[item])

            worksheet.write(f'B{i}', output, normal)

            # Supplemental Guidance
            output = ''
            if 'supplemental_guidance' in vulnerability:
                spg = vulnerability['supplemental_guidance']['ns2:div']
                for item in spg:
                    output += _xhtml_parser(item, spg[item])

            worksheet.write(f'C{i}', output, normal)

            # References
            output = ''
            if 'references' in vulnerability:
                ref = vulnerability['references']
                if type(ref) is bool:
                    output = ''
                elif type(ref) is list:
                    for item in ref:
                        output += f'{item["#text"]} ({item["@href"]}) \n'
                else:
                    output += f'{ref["#text"]} ({ref["@href"]}) \n'

            worksheet.write(f'D{i}', output, normal)

            # Control Enhancementes
            output = ''
            if 'control_enhancements' in vulnerability:
                coen = vulnerability['control_enhancements']
                if type(coen) is bool:
                    output = ''
                elif type(coen) is list:
                    for coen_item in coen:
                        output += f'{coen_item["@sequence"]}. \n'
                        if 'description' in coen_item:
                            desc = coen_item['description']['ns2:div']
                            output += 'Description: \n'
                            for item in desc:
                                output += _xhtml_parser(item, desc[item])
                        if 'supplemental-guidance' in coen_item:
                            spg = coen_item['supplemental-guidance']['ns2:div']
                            output += 'Supplemental Guidance: \n'
                            for item in spg:
                                output += _xhtml_parser(item, spg[item])
                        output += '\n'
                else:
                    if 'description' in coen:
                        desc = coen['description']['ns2:div']
                        output += 'Description: \n'
                        for item in desc:
                            output += _xhtml_parser(item, desc[item])
                    if 'supplemental-guidance' in coen:
                        spg = coen['supplemental-guidance']['ns2:div']
                        output += 'Supplemental Guidance: \n'
                        for item in spg:
                            output += _xhtml_parser(item, spg[item])

            worksheet.write(f'E{i}', output, normal)

        i += 1

    workbook.close()
    return file_name


if __name__ == "__main__":
    test = {
        'listing': [
            '{'
            '"AC-1":'
            '"AC-1 - Access Control Policy and Procedures - P1",'
            '"AC-4":'
            '"AC-4 - Information Flow Enforcement - P1",'
            '"AC-10":'
            '"AC-10 - Concurrent Session Control - P2",'
            '"AC-14":'
            '"AC-14 - Permitted Actions Without'
            ' Identification Or Authentication - P1",'
            '"AC-19":'
            '"AC-19 - Access Control for Mobile Devices - P1"'
            '}'
        ]
    }
    write(test)
    print('Generated test spreadsheet')
