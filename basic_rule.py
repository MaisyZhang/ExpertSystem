
class Rule:
    """
    前项通过 与 连接
    """
    def __init__(self, ants, con, desc=None):
        self.id = None
        self.antecedent = ants
        self.consequent = con
        self.description = desc

    def __str__(self):
        s = ''
        if self.description:
            s += ('Description: %s\n' % self.description)
        s += 'IF\t\t'
        for ant in self.antecedent:
            s += ('%s\n' % ant)
            if ant != self.antecedent[-1]:
                s += ('\tand\t')
        s += ('THEN\t%s\n' % self.consequent)
        return s


if __name__ == '__main__':
    # # 测试
    r = Rule(['检测食管24小时ph值阳性', '初步考虑胃食管返流病'], '考虑患者患有胃食管返流病', '建议消化科会诊，行抗返流治疗,进行肺功能相关检查')
    print(r)
    pass