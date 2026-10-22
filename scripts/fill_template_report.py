# -*- coding: utf-8 -*-
"""用学院官方模板填充出行天气助手课程论文。"""
import re
import shutil
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path(r'e:\Edownload\湖南农业大学课程论文格式模板.docx')
OUT = ROOT / 'docs' / '课程报告-出行天气助手.docx'
FIG = ROOT / 'docs' / 'figures'


def delete_element(el):
    parent = el.getparent()
    if parent is not None:
        parent.remove(el)


def set_run_font(run, east='宋体', ascii_font='Times New Roman', size=None, bold=None):
    run.font.name = ascii_font
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:ascii'), ascii_font)
    rFonts.set(qn('w:hAnsi'), ascii_font)
    rFonts.set(qn('w:eastAsia'), east)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold


def add_mixed_runs(paragraph, text, east='宋体', size=12, bold=False):
    parts = re.findall(r'[\u4e00-\u9fff]+|[^\u4e00-\u9fff]+', text)
    for part in parts:
        run = paragraph.add_run(part)
        if re.search(r'[\u4e00-\u9fff]', part):
            set_run_font(run, east=east, ascii_font='Times New Roman', size=size, bold=bold)
        else:
            set_run_font(run, east=east, ascii_font='Times New Roman', size=size, bold=bold)


def clear_runs(paragraph):
    for r in list(paragraph.runs):
        r._element.getparent().remove(r._element)


def set_left_tab(paragraph, pos_twips: int):
    pPr = paragraph._p.get_or_add_pPr()
    old = pPr.find(qn('w:tabs'))
    if old is not None:
        pPr.remove(old)
    tabs = OxmlElement('w:tabs')
    tab = OxmlElement('w:tab')
    tab.set(qn('w:val'), 'left')
    tab.set(qn('w:pos'), str(pos_twips))
    tabs.append(tab)
    pPr.append(tabs)


def fill_cover_line(paragraph, text, size=14):
    """封面字段统一四号宋体，避免中英文混排被拆成 Times New Roman。"""
    clear_runs(paragraph)
    run = paragraph.add_run(text)
    set_run_font(run, east='宋体', ascii_font='宋体', size=size, bold=False)


def disable_indent(p):
    p.paragraph_format.first_line_indent = Cm(0)
    pPr = p._p.get_or_add_pPr()
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        ind = OxmlElement('w:ind')
        pPr.append(ind)
    ind.set(qn('w:firstLine'), '0')
    ind.set(qn('w:firstLineChars'), '0')


def add_heading(doc, text, level):
    p = doc.add_paragraph(text, style=f'Heading {level}')
    for run in p.runs:
        set_run_font(run, east='黑体', ascii_font='Times New Roman', size={1: 15, 2: 14, 3: 12}[level], bold=False)
    return p


def add_body(doc, text):
    p = doc.add_paragraph(style='Normal')
    add_mixed_runs(p, text, east='宋体', size=12, bold=False)
    return p


def add_caption(doc, cn, en):
    p1 = doc.add_paragraph(style='Normal')
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    disable_indent(p1)
    add_mixed_runs(p1, cn, east='宋体', size=10.5, bold=False)
    p2 = doc.add_paragraph(style='Normal')
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    disable_indent(p2)
    add_mixed_runs(p2, en, east='宋体', size=10.5, bold=False)
    return p1, p2


def add_picture(doc, path, width_cm=12.5):
    p = doc.add_paragraph(style='Normal')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    disable_indent(p)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    run = p.add_run()
    run.add_picture(str(path), width=Cm(width_cm))
    return p


def shade_cell(cell, color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color)
    shd.set(qn('w:val'), 'clear')
    tcPr.append(shd)


def set_cell_border(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), '4')
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), '000000')
        borders.append(el)
    tcPr.append(borders)


def add_table(doc, headers, rows, caption_cn, caption_en):
    add_caption(doc, caption_cn, caption_en)
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = 1
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        disable_indent(p)
        run = p.add_run(h)
        set_run_font(run, east='黑体', size=10.5, bold=True)
        shade_cell(cell, 'D9E2F3')
        set_cell_border(cell)
    for r_i, row in enumerate(rows):
        for c_i, val in enumerate(row):
            cell = table.rows[r_i + 1].cells[c_i]
            cell.text = ''
            p = cell.paragraphs[0]
            disable_indent(p)
            add_mixed_runs(p, str(val), east='宋体', size=10.5)
            set_cell_border(cell)
    return table


def add_plain(doc, text, size=12):
    p = doc.add_paragraph(style='Normal')
    add_mixed_runs(p, text, east='宋体', size=size, bold=False)
    return p


def build():
    shutil.copyfile(TEMPLATE, OUT)
    doc = Document(str(OUT))

    paras = doc.paragraphs
    # 封面两栏用制表符对齐，班级为计算机24-2
    set_left_tab(paras[3], 5100)
    set_left_tab(paras[4], 5100)
    fill_cover_line(paras[3], '学  院：信息与智能科学技术学院\t班  级：计算机24-2')
    fill_cover_line(paras[4], '姓  名：黄奕轩\t学  号：202440210217')
    fill_cover_line(paras[5], '课程论文题目：基于HarmonyOS的出行天气助手设计与实现')
    fill_cover_line(paras[6], '课程名称：移动应用开发')

    # 删除封面之后的正文、表格（保留封面空行 P000-P024）
    for p in list(doc.paragraphs)[25:]:
        delete_element(p._element)
    for t in list(doc.tables):
        delete_element(t._tbl)

    # 题目
    p = doc.add_paragraph(style='Normal')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    disable_indent(p)
    run = p.add_run('基于HarmonyOS的出行天气助手设计与实现')
    set_run_font(run, east='黑体', ascii_font='黑体', size=18, bold=True)

    p = doc.add_paragraph(style='Normal')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    disable_indent(p)
    run = p.add_run('——面向短途出行的多城市天气查询应用')
    set_run_font(run, east='宋体', ascii_font='宋体', size=15, bold=False)

    p = doc.add_paragraph(style='Normal')
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    disable_indent(p)
    run = p.add_run('学    生：黄奕轩')
    set_run_font(run, east='宋体', ascii_font='宋体', size=10.5, bold=False)

    p = doc.add_paragraph(style='Normal')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    disable_indent(p)
    run = p.add_run('（信息与智能科学技术学院计算机24-2，学号202440210217）')
    set_run_font(run, east='宋体', ascii_font='宋体', size=10.5, bold=False)

    doc.add_paragraph(style='Normal')

    # 摘要
    p = doc.add_paragraph(style='Normal')
    run = p.add_run('摘  要：')
    set_run_font(run, east='黑体', size=12, bold=False)
    add_mixed_runs(
        p,
        '为解决短途出行前需反复切换城市查看天气的问题，设计并实现了一款HarmonyOS出行天气助手。系统采用ArkTS声明式UI与状态管理V2，通过Open-Meteo公开接口获取实时天气和七日预报，使用Navigation完成首页与详情页的路由传参及返回栈管理，并将天气卡片、温度柱状图封装为可复用组件。经DevEco Studio Previewer验证，应用能够完成加载提示、失败重试、空数据提示和图表随接口刷新，达到课程对网络交互、容器布局、自定义组件与版本管理的考核要求。',
        east='宋体',
        size=10.5,
        bold=False,
    )

    p = doc.add_paragraph(style='Normal')
    run = p.add_run('关键词：')
    set_run_font(run, east='黑体', size=12, bold=False)
    add_mixed_runs(p, 'HarmonyOS；ArkTS；Navigation；网络请求；数据可视化', east='宋体', size=10.5)

    add_heading(doc, '前言', 1)
    add_heading(doc, '项目背景', 2)
    add_body(
        doc,
        '出行前掌握目的地天气，是学生往返、短途旅行中的高频需求。现有做法多依赖浏览器或综合性天气应用，需要反复搜索城市，对比成本高，也不利于把课程中的布局、状态、路由和网络知识点串联起来。HarmonyOS以声明式UI和组件复用为主要开发方式，适合将“多城市对比”和“单城市详查”收敛到同一套轻量应用中。',
    )
    add_body(
        doc,
        '本课程要求独立完成可在Previewer中运行的综合项目，必须包含网络交互、Row/Column/List/Grid/Scroll容器、至少一个自定义组件、状态管理，以及不少于两个业务页面的Navigation跳转。据此，选题确定为出行天气助手：首页展示北京、上海、广州、成都、长沙、杭州六个出行城市的实时天气，详情页展示七日预报，并用柱状图绑定接口返回的最高气温。六个城市分别对应华北、华东、华南、西南、华中等常见出行方向，既避免功能空泛，也便于在Previewer窗口中完成对比。预期解决的问题包括远端数据如何稳定渲染、请求失败时如何给出可恢复反馈，以及系统路由表不支持Previewer时如何仍能完成多页跳转。',
    )

    add_heading(doc, '研究现状', 2)
    add_body(
        doc,
        '2019年华为发布HarmonyOS，提出面向全场景的分布式操作系统设计思路[1]。2024年HarmonyOS NEXT进一步将ArkTS声明式开发范式作为应用界面的主流写法，强调用状态驱动UI刷新[2]。在页面组织方面，官方文档提出以Navigation和NavPathStack替代传统router，完成多页面跳转、参数传递与返回栈管理[3]。网络访问方面，OpenHarmony提供@ohos.net.http模块，支持超时设置、状态码判断和请求对象销毁[4]。气象数据方面，Open-Meteo于2022年提供无需密钥的Forecast接口，可按经纬度返回当前天气与逐日预报，便于教学环境反复调试[5]。上述工作分别解决了系统平台、界面范式、路由、网络和数据源问题，但面向课程场景、且必须在Previewer中可演示的轻量出行天气应用仍需自行整合。本文在上述工作基础上完成需求、设计与实现。',
    )

    add_heading(doc, '需求分析', 1)
    add_body(
        doc,
        '目标用户为需要同时关注多个出行城市天气的在校学生和短途旅客，角色单一，用例集中在查询而非账户体系。用户打开应用后，应能对比多个城市的当前气温和天气现象；选中某一城市后进入详情，查看未来七天最高最低气温，并据此决定是否携带雨具。系统必须对网络失败、空数据给出明确提示，允许重试。用例关系如图2所示。',
    )
    add_picture(doc, FIG / 'fig-usecase.png', 13.5)
    add_caption(doc, '图 1 出行天气助手用例图', 'Fig.1 Use Case Diagram of Travel Weather Assistant')
    add_body(
        doc,
        '功能需求可归纳为：多城市实时天气总览、城市切换、手动刷新、加载/失败/空数据反馈、详情页七日预报、温度柱状图可视化，以及首页与详情页之间的参数传递与返回。非功能需求包括：仅依赖DevEco Studio Previewer、请求超时可感知、卡片组件可复用、Git按阶段提交以便复查。与记账、记事类题目相比，本选题没有登录注册页，界面复杂度集中在网络状态和多页传参，更贴近作业强调的硬性技术点。',
    )

    add_heading(doc, '系统概要设计', 1)
    add_heading(doc, '系统功能结构设计', 2)
    add_body(
        doc,
        '系统按业务页面划分为首页模块和详情页模块。首页负责城市选择、实时天气总览、网络状态反馈和手动刷新；详情页负责七日预报、温度柱状图以及基于路由栈的返回。可复用组件WeatherCard同时服务于两个页面，TempChart仅出现在详情页。功能结构如图2所示，图中只表示包含关系，不使用箭头。',
    )
    add_picture(doc, FIG / 'fig-func.png', 14.8)
    add_caption(doc, '图 2 系统功能结构图', 'Fig.2 System Functional Architecture Diagram')

    add_heading(doc, '技术选型', 2)
    add_body(
        doc,
        '开发工具为DevEco Studio，运行目标为HarmonyOS 5.0.0（API 12），语言为ArkTS。界面使用声明式UI，状态管理采用V2装饰器@ComponentV2、@Local、@Param和@Event，把页面内部状态与组件入参分开，避免子组件直接操作路由栈。路由使用Navigation与NavPathStack，并自定义PageMap以兼容Previewer。网络层直接使用系统能力@ohos.net.http，未引入Axios等第三方库。天气数据来自Open-Meteo Forecast接口，无需API Key，降低课堂环境下的配置成本。可视化未使用ECharts，而是用ArkUI容器按接口返回的最高气温数组绘制柱状图，保证Previewer中可运行且不增加额外依赖。',
    )

    add_heading(doc, '系统详细设计', 1)
    add_heading(doc, '首页详细设计', 2)
    add_heading(doc, '界面原型设计', 3)
    add_body(
        doc,
        '首页自上而下由标题行、城市Grid、当前城市WeatherCard和全部城市List构成，外层使用Scroll。标题行用Row放置应用名和刷新按钮。Grid三列展示六个城市，选中项改变背景色。WeatherCard内部再用Row和Column组合天气emoji、城市名、气温、湿度与风速，底部按钮通过@Event通知页面压入详情栈。List每项复用同一卡片，并开启nestedScroll以免与外层滚动冲突。加载中展示LoadingProgress，失败和空数据展示文案与重试按钮。首页原型如图3所示。',
    )
    add_picture(doc, FIG / 'fig-home-proto.png', 7.2)
    add_caption(doc, '图 3 首页原型设计图', 'Fig.3 Prototype of the Home Page')

    add_heading(doc, '数据接口设计', 3)
    add_body(doc, '首页按城市列表依次请求同一Forecast接口，经纬度来自本地常量CITY_LIST。接口说明如下。')
    add_plain(doc, '请求URL: https://api.open-meteo.com/v1/forecast')
    add_plain(doc, 'Http请求方式: GET')
    add_plain(doc, '数据交互格式：JSON')
    add_plain(doc, '请求参数：如表1所示')
    add_table(
        doc,
        ['请求字段', '必选', '类型及范围', '说明'],
        [
            ['latitude', 'True', 'number', '城市纬度，如长沙28.2282'],
            ['longitude', 'True', 'number', '城市经度，如长沙112.9388'],
            ['current', 'True', 'string', '当前天气字段列表'],
            ['daily', 'True', 'string', '逐日预报字段列表'],
            ['timezone', 'True', 'string', '时区，取Asia/Shanghai'],
            ['forecast_days', 'True', 'number', '预报天数，本系统取7'],
        ],
        '表1 首页请求参数详情表',
        'Table 1 Homepage Request Parameter Details',
    )
    add_plain(doc, '响应字段说明：如表2所示')
    add_table(
        doc,
        ['返回字段名', '字段类型', '字段说明'],
        [
            ['current.temperature_2m', 'number', '当前气温，单位℃'],
            ['current.relative_humidity_2m', 'number', '相对湿度，单位%'],
            ['current.weather_code', 'number', 'WMO天气代码'],
            ['current.wind_speed_10m', 'number', '风速，单位km/h'],
            ['daily.time', 'string[]', '预报日期数组'],
            ['daily.temperature_2m_max', 'number[]', '逐日最高气温'],
            ['daily.temperature_2m_min', 'number[]', '逐日最低气温'],
            ['daily.weather_code', 'number[]', '逐日天气代码'],
        ],
        '表2 首页响应参数详情表',
        'Table 2 Homepage Response Parameter Details',
    )

    add_heading(doc, '详情页详细设计', 2)
    add_heading(doc, '界面原型设计', 3)
    add_body(
        doc,
        '详情页在onReady中读取NavDestination传入的CityInfo。若缺少id，则进入空数据状态，不再发请求。成功后依次展示WeatherCard、TempChart和七日明细。TempChart根据最高气温的相对高低计算柱高，保证不同城市仍能看出趋势。明细每一行是Row，包含日期、天气现象和温度区间。返回由标题栏弹出路由栈完成。详情页原型如图4所示。',
    )
    add_picture(doc, FIG / 'fig-detail-proto.png', 7.2)
    add_caption(doc, '图 4 详情页原型设计图', 'Fig.4 Prototype of the Detail Page')

    add_heading(doc, '数据接口设计', 3)
    add_body(
        doc,
        '详情页复用WeatherService.fetchWeather，请求URL、方法、数据格式与首页相同，差别仅在于只请求路由传入的单个城市。请求参数仍如表1，响应字段仍如表2。页面用LoadStatus区分idle、loading、success、empty、error五态，HTTP非200、JSON缺字段或daily.time长度为0时进入失败或空数据分支，并提供重试。',
    )

    add_heading(doc, '系统实现', 1)
    add_heading(doc, '首页实现', 2)
    add_body(
        doc,
        '首页在aboutToAppear中调用loadAllCities。请求前将status置为loading；六个城市串行请求全部成功后渲染Grid、选中卡片和List；任一请求抛出异常则进入error并显示“重新加载”；预报日期数组为空则进入empty。WeatherService在finally中销毁HttpRequest，避免重复刷新造成资源泄漏。选中城市由@Local selectedCityId驱动，点击Grid即可切换高亮卡片。Previewer运行结果如图5所示。',
    )
    add_picture(doc, FIG / 'fig-home-impl.png', 7.2)
    add_caption(doc, '图 5 首页实现截图', 'Fig.5 Implementation Screenshot of the Home Page')

    add_heading(doc, '详情页实现', 2)
    add_body(
        doc,
        '首页点击“查看七日预报”时执行pushPathByName(\'DetailPage\', city)。详情页校验参数后再次请求该城市数据，将daily.time与temperature_2m_max绑定到TempChart，并将weather_code映射为中文现象后写入七日明细。标题显示为“长沙详情”等形式。若路由参数缺失，页面停留在空数据提示，避免对空对象继续访问网络。返回后首页保持原选中城市和已加载列表。实现截图如图6所示。',
    )
    add_picture(doc, FIG / 'fig-detail-impl.png', 7.2)
    add_caption(doc, '图 6 详情页实现截图', 'Fig.6 Implementation Screenshot of the Detail Page')

    add_heading(doc, '结论', 1)
    add_body(
        doc,
        '本文完成了面向短途出行的HarmonyOS天气查询应用。针对多城市对比和单城市详查两类需求，设计了首页与详情页的分工，并用CityInfo作为路由参数把二者联系起来。网络层将Open-Meteo返回的JSON映射为WeatherBundle，页面用LoadStatus区分加载、成功、空数据和失败，避免请求异常时界面无反馈。WeatherCard通过@Param和@Event成为纯展示组件，在首页选中区、城市列表和详情头部三处复用；TempChart把接口中的最高气温数组转成柱状图，满足动态数据可视化要求。开发中的主要取舍是路由方案：系统路由表更解耦，但官方说明其不支持Previewer，因此采用自定义PageMap，以保证作业规定的预览调试方式能够走通。',
    )
    add_body(
        doc,
        '后续工作可从三方面展开。一是将首页串行请求改为有限并发，并为每个城市提供独立加载态，缩短首屏等待。二是把写死的CITY_LIST扩展为搜索和定位，使应用从演示数据走向真实出行路径。三是在柱状图上叠加降水概率或体感温度，使可视化不仅展示气温高低，也能直接服务“是否带伞”的决策。工程上还可补充自动化界面测试，把loading、error、empty三条路径固化下来，减少答辩前回归成本。就课程目标而言，当前版本已经覆盖网络交互、容器布局、自定义组件、状态管理V2、Navigation传参和分阶段Git提交等考核点，可作为后续迭代的基础。',
    )

    p = doc.add_paragraph(style='Normal')
    disable_indent(p)
    run = p.add_run('参考文献')
    set_run_font(run, east='黑体', size=15, bold=False)

    refs = [
        '[1] 华为技术有限公司. HarmonyOS系统介绍[EB/OL]. (2019)[2026-10-22]. https://www.harmonyos.com/.',
        '[2] 华为技术有限公司. ArkUI声明式开发范式[EB/OL]. (2024)[2026-10-22]. https://developer.huawei.com/consumer/cn/doc/.',
        '[3] 华为技术有限公司. Navigation与NavPathStack[EB/OL]. (2024)[2026-10-22]. https://developer.huawei.com/consumer/cn/doc/.',
        '[4] OpenHarmony. @ohos.net.http 接口说明[EB/OL]. (2024)[2026-10-22]. https://gitee.com/openharmony/docs.',
        '[5] Zippenfenig G. Open-Meteo: Weather Forecast API Documentation[EB/OL]. (2022)[2026-10-22]. https://open-meteo.com/.',
    ]
    for item in refs:
        p = doc.add_paragraph(style='Normal')
        p.paragraph_format.first_line_indent = Cm(-0.74)
        pPr = p._p.get_or_add_pPr()
        ind = pPr.find(qn('w:ind'))
        if ind is None:
            ind = OxmlElement('w:ind')
            pPr.append(ind)
        ind.set(qn('w:left'), '148')
        ind.set(qn('w:firstLine'), '-148')
        add_mixed_runs(p, item, east='宋体', size=10.5)

    p = doc.add_paragraph(style='Normal')
    disable_indent(p)
    run = p.add_run('附件')
    set_run_font(run, east='仿宋_GB2312', size=14, bold=True)

    p = doc.add_paragraph(style='Normal')
    disable_indent(p)
    add_mixed_runs(p, '项目gitk的截图', east='仿宋_GB2312', size=14, bold=False)
    add_picture(doc, FIG / 'fig-gitk.png', 15.2)
    add_caption(doc, '图 7 项目Git提交记录', 'Fig.7 Git Commit History of the Project')

    doc.save(str(OUT))
    print('wrote', OUT)


if __name__ == '__main__':
    build()
