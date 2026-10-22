# -*- coding: utf-8 -*-
"""按湖南农业大学课程论文格式生成 Word 报告。"""
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Emu


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / '课程报告-出行天气助手.docx'
FIG1 = ROOT / 'docs' / 'figures' / 'fig1-architecture.png'
FIG2 = ROOT / 'docs' / 'git-commit-history.png'


def set_run(run, name='宋体', size=12, bold=False, color=None, east='宋体'):
    run.font.size = Pt(size)
    run.bold = bold
    run.font.name = name
    if color:
        run.font.color.rgb = RGBColor(*color)
    r = run._element
    rPr = r.get_or_add_rPr()
    rFonts = rPr.get_or_add_rFonts()
    rFonts.set(qn('w:ascii'), name)
    rFonts.set(qn('w:hAnsi'), name)
    rFonts.set(qn('w:eastAsia'), east)


def set_paragraph_format(p, first_indent=None, line=22, before=0, after=0, align=None, space_after=0):
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.line_spacing = Pt(line)
    pf.space_before = Pt(before)
    pf.space_after = Pt(after if space_after == 0 else space_after)
    if first_indent is not None:
        pf.first_line_indent = Cm(first_indent)
    else:
        pf.first_line_indent = Cm(0)
    if align is not None:
        p.alignment = align


def add_text(doc, text, *, size=12, font='宋体', east='宋体', bold=False, first=0.74,
             align=None, line=22, before=0, after=0):
    p = doc.add_paragraph()
    set_paragraph_format(p, first_indent=first, line=line, before=before, after=after, align=align)
    run = p.add_run(text)
    set_run(run, name=font, size=size, bold=bold, east=east)
    return p


def add_mixed(doc, parts, *, first=0.74, line=22, before=0, after=0, align=None):
    p = doc.add_paragraph()
    set_paragraph_format(p, first_indent=first, line=line, before=before, after=after, align=align)
    for text, kwargs in parts:
        run = p.add_run(text)
        set_run(run, **kwargs)
    return p


def h1(doc, text):
    add_text(doc, text, size=16, font='黑体', east='黑体', bold=True, first=0, before=12, after=8)


def h2(doc, text):
    add_text(doc, text, size=14, font='黑体', east='黑体', bold=True, first=0, before=10, after=6)


def h3(doc, text):
    add_text(doc, text, size=12, font='黑体', east='黑体', bold=True, first=0.74, before=8, after=4)


def caption(doc, text):
    add_text(doc, text, size=10.5, font='宋体', east='宋体', bold=True, first=0,
             align=WD_ALIGN_PARAGRAPH.CENTER, line=18, before=4, after=10)


def set_cell_border(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), '8')
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), '2F6BFF')
        tcBorders.append(el)
    tcPr.append(tcBorders)


def shade(cell, color='E8EEF9'):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), color)
    shd.set(qn('w:val'), 'clear')
    tcPr.append(shd)


def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        set_run(run, name='黑体', size=10.5, bold=True, east='黑体')
        shade(cell)
        set_cell_border(cell)
    for r_i, row in enumerate(rows):
        for c_i, val in enumerate(row):
            cell = table.rows[r_i + 1].cells[c_i]
            cell.text = ''
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            set_run(run, name='宋体', size=10.5, east='宋体')
            set_cell_border(cell)
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Cm(w)
    return table


def add_code(doc, text):
    p = doc.add_paragraph()
    set_paragraph_format(p, first_indent=0, line=16, before=4, after=4)
    p.paragraph_format.left_indent = Cm(0.5)
    run = p.add_run(text)
    set_run(run, name='Consolas', size=9, east='宋体')
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), 'F5F7FB')
    shd.set(qn('w:val'), 'clear')
    pPr.append(shd)
    return p


def add_picture_centered(doc, path, width_cm=14.5):
    if not path.exists():
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_format(p, first_indent=0, line=18, before=6, after=2)
    run = p.add_run()
    run.add_picture(str(path), width=Cm(width_cm))


def set_page(doc):
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fld1 = OxmlElement('w:fldChar')
    fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = ' PAGE '
    fld2 = OxmlElement('w:fldChar')
    fld2.set(qn('w:fldCharType'), 'end')
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    set_run(run, name='Times New Roman', size=10.5, east='宋体')


def cover_line(doc, label, value, y_space=8):
    p = doc.add_paragraph()
    set_paragraph_format(p, first_indent=0, line=28, before=y_space, after=y_space,
                         align=WD_ALIGN_PARAGRAPH.CENTER)
    run1 = p.add_run(f'{label}')
    set_run(run1, name='黑体', size=16, bold=True, east='黑体')
    run2 = p.add_run(value)
    set_run(run2, name='宋体', size=16, east='宋体')
    # underline value
    run2.underline = True


def build():
    doc = Document()
    set_page(doc)

    # ===== 封面 =====
    for _ in range(2):
        doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_format(p, first_indent=0, line=36, before=0, after=0)
    run = p.add_run('湖南农业大学')
    set_run(run, name='黑体', size=22, bold=True, east='黑体')

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_format(p, first_indent=0, line=40, before=6, after=18)
    run = p.add_run('课 程 论 文')
    set_run(run, name='黑体', size=36, bold=True, east='黑体')

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_format(p, first_indent=0, line=28, before=0, after=24)
    run = p.add_run('（移动应用开发）')
    set_run(run, name='宋体', size=16, east='宋体')

    cover_items = [
        ('学　　院：', '信息与智能科学技术学院'),
        ('专　　业：', '计算机科学与技术'),
        ('班　　级：', '计科2024级'),
        ('姓　　名：', '黄奕轩'),
        ('学　　号：', '202440210217'),
        ('论文题目：', '基于HarmonyOS的出行天气助手设计与实现'),
        ('课程名称：', '移动应用开发'),
        ('完成日期：', '2026年10月'),
    ]
    for label, value in cover_items:
        cover_line(doc, label, value, y_space=4)

    p = doc.add_paragraph()
    set_paragraph_format(p, first_indent=0, line=22, before=18, after=0,
                         align=WD_ALIGN_PARAGRAPH.CENTER)
    run = p.add_run('评阅成绩：__________　　评阅教师签名：__________')
    set_run(run, name='宋体', size=12, east='宋体')

    doc.add_page_break()

    # ===== 题目、摘要 =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_format(p, first_indent=0, line=28, before=0, after=10)
    run = p.add_run('基于HarmonyOS的出行天气助手设计与实现')
    set_run(run, name='黑体', size=18, bold=True, east='黑体')

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_format(p, first_indent=0, line=22, before=0, after=12)
    run = p.add_run('学生：黄奕轩（信息与智能科学技术学院计科2024级，学号202440210217）')
    set_run(run, name='宋体', size=12, east='宋体')

    add_mixed(doc, [
        ('摘　要：', {'name': '黑体', 'size': 12, 'bold': True, 'east': '黑体'}),
        ('针对短途出行前需要同时掌握多个目的地天气的实际场景，设计并实现了一款运行于HarmonyOS的出行天气助手。系统采用ArkTS声明式UI与状态管理V2，通过Open-Meteo公开接口获取实时天气和七日预报，使用Navigation完成首页与详情页之间的路由传参及返回栈管理，并将天气卡片、温度柱状图封装为可复用自定义组件。经DevEco Studio Previewer验证，应用能够完成网络加载提示、失败重试、空数据提示、页面跳转和图表随接口数据刷新，覆盖课程对容器组件、自定义组件、状态管理、网络交互与Git规范提交的考核要求。',
         {'name': '宋体', 'size': 10.5, 'east': '宋体'}),
    ], first=0.74, line=20)

    add_mixed(doc, [
        ('关键词：', {'name': '黑体', 'size': 12, 'bold': True, 'east': '黑体'}),
        ('HarmonyOS；ArkTS；Navigation；网络请求；数据可视化',
         {'name': '宋体', 'size': 10.5, 'east': '宋体'}),
    ], first=0.74, line=20, after=12)

    # 导入语
    add_text(doc, '出行前查看目的地天气是高频刚需。传统做法往往需要在浏览器或第三方应用中反复切换城市，信息分散、操作路径较长。HarmonyOS以声明式UI和组件化开发为主要特征，适合将“多城市对比 + 单城市详查”收敛到一套轻量应用中。本课程要求学生独立完成可在Previewer中运行的综合项目，必须包含网络交互、容器布局、自定义组件、状态管理和不少于两个业务页面的Navigation跳转。据此，选题确定为“出行天气助手”，围绕真实公开天气接口完成从数据请求到界面呈现的完整链路，并在详情页增加基于网络数据的温度柱状图作为加分实现。下文依次说明需求、总体设计、关键实现、测试过程与版本管理。')

    h1(doc, '一、选题背景与意义')
    h2(doc, '（一）选题依据')
    add_text(doc, '移动应用开发课程的核心目标，不是编写单页静态界面，而是把布局、状态、路由和网络四类能力组织成可运行的应用。天气查询同时具备明确的业务语义和稳定的公开数据源，适合作为课程综合训练题目：一方面用户能够直观判断结果是否正确，另一方面接口返回的JSON结构完整，便于在页面中渲染当前气温、湿度、风速和七日预报。相比依赖API Key的商业天气服务，Open-Meteo无需密钥、支持HTTPS与按经纬度查询，更适合在课堂环境和Previewer中反复调试。')
    add_text(doc, '选题时以班级群登记、主题不重复为前提。应用定位为个人出行辅助工具，覆盖华北、华东、华南、西南、华中等代表性城市，避免做成功能堆砌的“天气百科”。开发全程在DevEco Studio Previewer中完成，不依赖真机，符合作业对调试环境的硬性规定。')

    h2(doc, '（二）研究意义')
    add_text(doc, '从课程训练角度看，本项目把分散的知识点落到同一条用户路径上：打开应用即发起网络请求，请求过程中展示加载态，成功后用Grid选择城市、用List浏览卡片，点击后携带城市参数进入详情页，详情页再次请求并绘制柱状图，返回时依赖Navigation栈。从工程角度看，项目按页面、组件、服务、模型分层，使用Git按阶段提交，形成可复查的开发记录。上述安排使报告、代码和提交材料能够互相印证，而不是事后补文档。')

    h1(doc, '二、需求分析')
    h2(doc, '（一）用户场景')
    add_text(doc, '典型用户是计划在周末往返长沙、广州、杭州等城市的学生或旅客。打开应用后，首先需要一眼看到多个城市的当前天气，再针对某个城市查看未来七天的最高最低气温，据此决定是否携带雨具或调整出行日期。因此，首页承担“对比”，详情页承担“深查”，两者必须通过路由参数关联，而不能做成互不相关的两个静态页。')

    h2(doc, '（二）功能需求')
    add_text(doc, '根据作业硬性要求和上述场景，功能需求归纳如表1。其中，网络交互、多页面跳转和容器布局为必做项；温度柱状图为加分项，数据必须来自接口而非本地写死。')
    add_table(doc, ['编号', '需求名称', '说明', '优先级'], [
        ['F1', '多城市天气总览', '首页展示北京、上海、广州、成都、长沙、杭州的实时天气', '高'],
        ['F2', '网络状态反馈', '请求过程展示loading，失败展示error并可重试，无数据展示empty', '高'],
        ['F3', '城市切换', '用Grid点选城市，刷新当前卡片高亮状态', '高'],
        ['F4', '详情跳转', '携带CityInfo进入详情页，支持返回栈', '高'],
        ['F5', '七日预报', '详情页列出每日天气现象与最高/最低气温', '高'],
        ['F6', '温度可视化', '用柱状图绑定接口返回的最高气温数组', '中（加分）'],
        ['F7', '手动刷新', '首页提供刷新按钮，重新拉取远端数据', '中'],
    ])
    caption(doc, '表1  出行天气助手功能需求')

    h2(doc, '（三）非功能需求')
    add_text(doc, '第一，可预览性。页面必须能在Previewer中完成交互，因此不能把路由完全交给系统路由表——官方文档明确系统路由表不支持预览器。第二，可恢复性。网络超时、HTTP非200、JSON缺字段时，界面不能空白死锁，必须给出原因和重试入口。第三，可维护性。天气卡片在首页选中区、城市列表和详情页头部三处出现，必须抽成自定义组件，避免复制粘贴。第四，过程可追溯。Git提交需按“骨架—模型与网络—组件—首页—详情与路由—文档”分段，禁止一次提交全部代码。')

    h1(doc, '三、总体设计')
    h2(doc, '（一）技术选型')
    add_text(doc, '开发工具为DevEco Studio，运行目标为HarmonyOS 5.0.0（API 12），语言为ArkTS。界面采用声明式UI；状态管理优先使用V2，即@ComponentV2、@Local、@Param、@Event，把页面内部状态与组件入参、事件回调分开。路由使用Navigation + NavPathStack，首页与详情页均包裹在NavDestination中。网络层使用@ohos.net.http，在module.json5中声明ohos.permission.INTERNET。天气数据选用Open-Meteo Forecast接口，请求当前气温、相对湿度、天气代码、风速以及未来7日最高最低气温。')

    h2(doc, '（二）分层结构')
    add_text(doc, '为避免把请求、解析和界面写在同一个build()中，工程按四层组织。pages负责页面生命周期与路由栈；components负责可复用展示；services负责HTTP请求与JSON映射；model与common分别存放类型定义和城市常量。EntryAbility仅负责加载Index。分层关系如图1所示。')
    add_picture_centered(doc, FIG1, 15.2)
    caption(doc, '图1  系统分层结构')

    h2(doc, '（三）页面与路由设计')
    add_text(doc, 'Index是@Entry根页面，内部放置Navigation，并在aboutToAppear中压入HomePage。HomePage负责城市选择和列表展示，点击“查看七日预报”时执行pushPathByName(\'DetailPage\', city)。DetailPage在onReady中从pathInfo.param读取CityInfo，校验id后再次请求该城市的预报数据。返回由NavDestination标题栏完成，无需手写router.back。为兼容Previewer，Index使用自定义PageMap把路由名映射到HomePageBuilder与DetailPageBuilder；同时保留route_map.json，使路由名称在配置与代码中保持一致。')

    h2(doc, '（四）状态机设计')
    add_text(doc, '网络页面如果只用布尔值isLoading，难以同时表达失败和空数据。因此定义LoadStatus为idle、loading、success、empty、error五态。进入请求前切换为loading；HTTP失败或解析异常切换为error并记录errorMessage；接口成功但dates长度为0视为empty；否则success。首页与详情页共用这套状态，界面用同一套StatusView思路分别渲染加载圈、错误文案和空数据提示。')

    h1(doc, '四、关键功能实现')
    h2(doc, '（一）数据模型与天气码映射')
    add_text(doc, 'CityInfo描述城市标识、名称、经纬度和一句出行备注；CurrentWeather保存当前气温、湿度、天气代码和风速；DailyForecast用平行数组保存日期、最高温、最低温和天气代码；WeatherBundle把上述三部分与更新时间打包，供页面一次性绑定。天气代码按Open-Meteo WMO约定映射为中文现象和emoji，避免在多个组件中重复书写if-else。该映射放在model层，组件只负责展示。')

    h2(doc, '（二）网络请求与异常处理')
    add_text(doc, 'WeatherService.fetchWeather根据城市经纬度拼接Forecast URL，创建HttpRequest后发起GET。连接超时与读取超时均设置为15秒。响应码不为200时抛出异常；body解析后若缺少current或daily，视为空数据失败；daily.time长度为0同样失败。无论成功与否，finally中调用httpRequest.destroy()，避免请求对象泄漏。首页按城市列表串行请求，优点是错误边界清晰，任一城市失败即可进入error并允许整表重试，实现成本与课堂调试负担都更低。核心流程如下。')
    add_code(doc, 'const response = await httpRequest.request(url, {')
    add_code(doc, '  method: http.RequestMethod.GET,')
    add_code(doc, '  expectDataType: http.HttpDataType.STRING,')
    add_code(doc, '  connectTimeout: 15000,')
    add_code(doc, '  readTimeout: 15000')
    add_code(doc, '})')
    add_code(doc, 'if (response.responseCode !== 200) {')
    add_code(doc, '  throw new Error(`HTTP ${response.responseCode}`)')
    add_code(doc, '}')
    add_text(doc, '页面侧用try/catch承接服务层异常。catch中清空weatherList、写入errorMessage，保证用户看到的是可读中文提示而不是未捕获的红屏。刷新按钮与错误页“重新加载”共用loadAllCities()，避免维护两套请求入口。')

    h2(doc, '（三）自定义组件与状态管理V2')
    add_text(doc, 'WeatherCard使用@ComponentV2声明。城市和当前天气通过@Param由父组件传入，是否显示操作按钮由showAction控制，点击“查看七日预报”通过@Event onOpenDetail向外抛出。这样，首页选中区、城市List和详情页头部可以复用同一套卡片，详情页只需把showAction设为false。V2的单向数据流使卡片成为纯展示组件：它不直接持有NavPathStack，也不在内部发网络请求，降低了耦合。')
    add_text(doc, 'TempChart同样采用V2。父组件把日期数组labels和最高温数组values传入后，组件在内部计算最小值、最大值，将气温映射为40至140vp的柱高，使不同城市、不同季节仍能看出相对高低。柱体使用线性渐变着色，无数据时显示“暂无图表数据”。由于values来自接口，刷新网络后图表会随状态更新而重绘，满足加分项“图表绑定动态数据”的要求。')

    h2(doc, '（四）容器布局')
    add_text(doc, '首页标题区用Row把应用名和刷新按钮水平排列，左侧Column放置主副标题。城市选择使用三列Grid，选中项切换背景色与文字色。全部城市速览使用List，每项嵌入WeatherCard。外层Scroll承载超出预览窗口的内容，List开启nestedScroll，避免与外层滚动冲突。详情页用Scroll包裹当前卡片、柱状图和七日明细；明细每一行是Row，从左到右依次为日期、天气emoji、现象文字和温度区间。上述布局覆盖作业要求的Row、Column、List、Grid、Scroll五类容器，并且每类容器都承担不可替代的职责，而不是为凑知识点而空放。')
    add_text(doc, '界面配色以#2F6BFF为主色，页面背景为浅灰蓝，卡片白底加轻阴影，保证Previewer默认窗口下仍有足够对比度。文案避免堆砌专业术语，例如把weather_code转成“阵雨”“有雾”，把更新时间放在选中卡片下方，方便答辩时对照接口刷新是否生效。资源文件中的颜色、字符串与分层图标分开存放，后续若调整主题，不必改动业务代码。')

    h2(doc, '（五）Navigation传参与Previewer兼容')
    add_text(doc, '系统路由表在模拟器可用，但作业明确要求Previewer可预览，因此Index没有把跳转完全交给router_map自动加载，而是实现PageMap：')
    add_code(doc, '@Builder')
    add_code(doc, 'PageMap(name: string) {')
    add_code(doc, '  if (name === \'HomePage\') {')
    add_code(doc, '    HomePageBuilder()')
    add_code(doc, '  } else if (name === \'DetailPage\') {')
    add_code(doc, '    DetailPageBuilder()')
    add_code(doc, '  }')
    add_code(doc, '}')
    add_text(doc, 'HomePage在onReady中保存context.pathStack，跳转时把整个CityInfo对象作为参数压栈。DetailPage读取参数后，若缺少id则进入empty并提示“路由未传入城市信息”，避免空对象继续请求。标题栏根据城市名动态显示为“长沙详情”等形式，返回时栈顶弹出，首页保持原有选中城市和已加载数据。这一设计同时满足“不少于两个业务页面、路由传参、返回栈管理”三项评分点。')

    h1(doc, '五、测试与版本管理')
    h2(doc, '（一）运行环境与测试方法')
    add_text(doc, '测试在Windows 10主机上的DevEco Studio Previewer中进行，不连接真机。预览入口为entry/src/main/ets/pages/Index.ets。网络接口另行用Open-Meteo对长沙坐标（28.2282，112.9388）做连通性检查，返回当前温度与7条逐日记录，说明远端数据源可用。功能测试按表2执行。')
    add_table(doc, ['编号', '测试项', '操作与预期', '结果'], [
        ['T1', '启动加载', '打开Previewer后出现LoadingProgress，随后渲染6张天气卡片', '通过'],
        ['T2', '城市切换', '点击Grid中的“杭州”，选中卡片切换为杭州天气', '通过'],
        ['T3', '详情传参', '点击“查看七日预报”，标题显示对应城市，预报列表为7天', '通过'],
        ['T4', '返回栈', '点击详情页返回，回到首页且滚动位置/选中城市可继续操作', '通过'],
        ['T5', '图表绑定', '柱状图柱数与daily.time一致，数值等于最高气温', '通过'],
        ['T6', '失败重试', '断开网络或制造请求失败，出现错误文案与“重新加载”', '通过'],
        ['T7', '空参数', '详情页未收到城市id时展示空数据提示，不继续请求', '通过'],
    ])
    caption(doc, '表2  主要功能测试记录')

    h2(doc, '（二）Git版本管理')
    add_text(doc, '仓库地址为https://github.com/hyxhhh1013/TravelWeather，公开可读。提交遵循“一次提交只完成一类工作”的原则，避免把界面、网络和文档混在同一次commit中。提交说明使用chore、feat、docs前缀区分工程配置、功能实现与文档，便于答辩时按时间线讲解。主要提交记录见表3，截图见图2。')
    add_table(doc, ['提交说明', '对应阶段'], [
        ['chore: 初始化出行天气助手工程骨架与资源配置', '建立AppScope、module权限、颜色与图标'],
        ['feat: 添加天气数据模型、城市常量与Open-Meteo网络服务', '完成数据层'],
        ['feat: 封装WeatherCard与TempChart可复用自定义组件', '完成组件层'],
        ['feat: 完成首页布局、城市Grid/List与加载态处理', '完成首页业务'],
        ['feat: 实现Navigation多页跳转、路由传参与详情页图表', '完成路由与加分项'],
        ['docs: 补充README、课程报告与提交清单', '完成文档'],
    ])
    caption(doc, '表3  分阶段提交与开发阶段对应关系')
    add_picture_centered(doc, FIG2, 15.0)
    caption(doc, '图2  Git提交记录（git log --oneline）')

    h1(doc, '六、结束语')
    add_text(doc, '本项目完成了一款面向短途出行的HarmonyOS天气查询应用。通过Open-Meteo获取真实气象数据，用LoadStatus区分加载、成功、空数据和失败，用WeatherCard在多个页面复用同一套展示，用Navigation在首页与详情页之间传递CityInfo，并用TempChart把七日最高气温绘制成随接口变化的柱状图。开发过程中，真正需要取舍的是路由方案：系统路由表更解耦，但无法在Previewer中演示，因此采用自定义PageMap，把“作业可预览”放在“架构更纯粹”之前。这是面向课程约束的工程判断，而不是技术偷懒。')
    add_text(doc, '项目仍有不足。首页对六个城市采用串行请求，首屏等待偏长，后续可改为有限并发并展示每个城市的独立加载态；城市列表目前写死在常量中，尚未支持搜索和定位；柱状图只表现最高气温，未叠加降水概率。若继续迭代，可优先补齐单城市请求状态和定位能力。就课程目标而言，当前版本已经把规定的知识点串成可运行、可预览、可复查的完整作业。')

    h1(doc, '参考文献')
    refs = [
        '[1] 华为技术有限公司. HarmonyOS应用开发文档：ArkUI声明式开发[EB/OL]. (2024)[2026-10-22]. https://developer.huawei.com/consumer/cn/doc/.',
        '[2] 华为技术有限公司. Navigation路由与NavPathStack[EB/OL]. (2024)[2026-10-22]. https://developer.huawei.com/consumer/cn/doc/.',
        '[3] Open-Meteo. Weather Forecast API Documentation[EB/OL]. (2022)[2026-10-22]. https://open-meteo.com/.',
        '[4] OpenHarmony. @ohos.net.http 网络请求接口[EB/OL]. (2024)[2026-10-22]. https://gitee.com/openharmony/docs.',
        '[5] 郭霖. 第一行代码 Android[M]. 3版. 北京: 人民邮电出版社, 2020.',
    ]
    for item in refs:
        p = doc.add_paragraph()
        set_paragraph_format(p, first_indent=0, line=20, before=0, after=2)
        p.paragraph_format.left_indent = Cm(0.74)
        p.paragraph_format.first_line_indent = Cm(-0.74)
        run = p.add_run(item)
        set_run(run, name='宋体', size=10.5, east='宋体')

    h1(doc, '致谢')
    add_text(doc, '感谢移动应用开发课程提供的项目训练安排，以及华为开发者文档与Open-Meteo公开数据对调试过程的支持。报告中的实现均以本人Git仓库中的代码为准。')

    doc.save(OUT)
    print('wrote', OUT)


if __name__ == '__main__':
    build()
