#!/usr/bin/python
# encoding:utf-8

import re
from basic_rule import Rule
rules_filepath = 'rules.txt'

re_a_rule = re.compile(r'(\{.*?\})')
re_if_part = re.compile(r'^\{IF:\s+(\[.*?\])')
re_then_part = re.compile(r'THEN:\s+(\'.*?\')')
re_description_part = re.compile(r'DESCRIPTION:\s+(\'.*?\')')


def generate_a_rule(rule):
    if_part_list = (re_if_part.findall(rule)[0]).split('\'')
    del(if_part_list[0])
    del(if_part_list[-1])
    if_part_temp = ''.join(if_part_list)
    if_part = if_part_temp.split(',')
    then_part = re_then_part.findall(rule)[0]
    description_part = re_description_part.findall(rule)[0]
    return Rule(if_part, then_part.strip('"\''), description_part.strip('"\''))


def separate_rules(rules):
    rule_group = re_a_rule.findall(rules)
    return list(map(generate_a_rule, rule_group))


def read_rules(rules_filepath):
    with open(rules_filepath, 'r', encoding='UTF-8') as f:
        rules = ''.join(f.read().splitlines())
    return separate_rules(rules)


def inference(rules, facts):
    candidate_rule = []
    visited_rule = []
    infer_rules = []
    results = []
    flag = False

    while True:
        candidate_rule.clear()
        for rule in rules:
            if list_in_set(rule.antecedent, facts) and rule not in visited_rule:
                candidate_rule.append(rule)
                visited_rule.append(rule)
                temp = '规约：{key}---->{value}'.format(key=rule.antecedent, value=rule.consequent)
                infer_rules.append(temp)

        if len(candidate_rule) != 0:
            result = resolve(candidate_rule)
            facts.append(result.consequent)
            results.append(result.description)
            flag = True
            temp1 = '冲突消解：{key}---->{value}'.format(key=result.antecedent, value=result.consequent)
            infer_rules.append(temp1)
        else:
            break

    if flag is False:
        results = None

    return results, infer_rules, visited_rule


def list_in_set(list, set):
    for i in list:
        if i not in set:
            return False
    return True


def resolve(candidate_rule):
    return candidate_rule[-1]


def main():
    # 以下为测试内容
    facts = ['胸闷 气急 烧心 反胃', '检测食管24小时ph值阳性']
    rules = read_rules(rules_filepath)
    results, hit_rules, visited_rules = inference(rules, facts)
    print(results)
    print(hit_rules)
    s = ''
    for rule in visited_rules:
        s += str(rule)

    print(s)


    pass

if __name__ == '__main__':
    main()