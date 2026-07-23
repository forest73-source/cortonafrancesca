import json, re

d = json.load(open("/app/frontend/src/data/content.json"))

L = ["en", "es", "fr", "zh"]

# phrase -> {en,es,fr,zh}; applied longest-first with placeholder protection
PH = {
  "l' incredulita di san tommaso": {"en":"The Incredulity of Saint Thomas","es":"La incredulidad de Santo Tomás","fr":"L'incrédulité de saint Thomas","zh":"圣托马斯的怀疑"},
  "la mano di dio in la creazione di adamo": {"en":"The Hand of God in the Creation of Adam","es":"La mano de Dios en la creación de Adán","fr":"La main de Dieu dans la création d'Adam","zh":"《创造亚当》中上帝之手"},
  "glifo del sole e della terra": {"en":"Glyph of the Sun and the Earth","es":"Glifo del Sol y de la Tierra","fr":"Glyphe du Soleil et de la Terre","zh":"太阳与大地的符号"},
  "glifo della luna e del quadrato": {"en":"Glyph of the Moon and the Square","es":"Glifo de la Luna y del cuadrado","fr":"Glyphe de la Lune et du carré","zh":"月亮与方形的符号"},
  "glifo di nettuno": {"en":"Glyph of Neptune","es":"Glifo de Neptuno","fr":"Glyphe de Neptune","zh":"海王星符号"},
  "glifo di plutone": {"en":"Glyph of Pluto","es":"Glifo de Plutón","fr":"Glyphe de Pluton","zh":"冥王星符号"},
  "glifo di venere": {"en":"Glyph of Venus","es":"Glifo de Venus","fr":"Glyphe de Vénus","zh":"金星符号"},
  "l' universo l'infinito": {"en":"The Universe, the Infinite","es":"El Universo, el Infinito","fr":"L'Univers, l'Infini","zh":"宇宙，无限"},
  "luna piena": {"en":"Full Moon","es":"Luna llena","fr":"Pleine Lune","zh":"满月"},
  "sacro cuore": {"en":"Sacred Heart","es":"Sagrado Corazón","fr":"Sacré-Cœur","zh":"圣心"},
  "opera in beneficenza per il progetto": {"en":"charity work for the project","es":"obra benéfica para el proyecto","fr":"œuvre caritative pour le projet","zh":"为项目创作的慈善作品"},
  "progettazione": {"en":"Study","es":"Estudio","fr":"Étude","zh":"草图"},

  "dipinto ad olio e pigmento fotoluminoscente": {"en":"oil and photoluminescent pigment,","es":"óleo y pigmento fotoluminiscente,","fr":"huile et pigment photoluminescent,","zh":"油画与光致发光颜料，"},
  "dipinto a olio e pigmento fotoluminoscente": {"en":"oil and photoluminescent pigment,","es":"óleo y pigmento fotoluminiscente,","fr":"huile et pigment photoluminescent,","zh":"油画与光致发光颜料，"},
  "dipinto olio e pigmento fotoluminoscente": {"en":"oil and photoluminescent pigment,","es":"óleo y pigmento fotoluminiscente,","fr":"huile et pigment photoluminescent,","zh":"油画与光致发光颜料，"},
  "dipinto a olio fotoluminescente": {"en":"photoluminescent oil,","es":"óleo fotoluminiscente,","fr":"huile photoluminescente,","zh":"光致发光油彩，"},
  "olio e pigmento fotoluminoscente": {"en":"oil and photoluminescent pigment,","es":"óleo y pigmento fotoluminiscente,","fr":"huile et pigment photoluminescent,","zh":"油画与光致发光颜料，"},

  "effetto di giorno il pigmento risulta neutro": {"en":"— by day the pigment appears neutral","es":"— de día el pigmento resulta neutro","fr":"— de jour le pigment est neutre","zh":"— 白天颜料呈中性"},
  "effetto del giorno il pigmento risulta neutro": {"en":"— by day the pigment appears neutral","es":"— de día el pigmento resulta neutro","fr":"— de jour le pigment est neutre","zh":"— 白天颜料呈中性"},
  "effetto al buio il pigmento si illumina": {"en":"— in the dark the pigment glows","es":"— en la oscuridad el pigmento se ilumina","fr":"— dans l'obscurité le pigment s'illumine","zh":"— 黑暗中颜料发光"},
  "effetto al buoi il pigmento si illumina": {"en":"— in the dark the pigment glows","es":"— en la oscuridad el pigmento se ilumina","fr":"— dans l'obscurité le pigment s'illumine","zh":"— 黑暗中颜料发光"},

  "su lamiera zincata": {"en":"on galvanized sheet metal","es":"sobre chapa galvanizada","fr":"sur tôle galvanisée","zh":"于镀锌金属板"},
  "su lamiera": {"en":"on sheet metal","es":"sobre chapa","fr":"sur tôle","zh":"于金属板"},
  "olio su marmo di carrara": {"en":"oil on Carrara marble","es":"óleo sobre mármol de Carrara","fr":"huile sur marbre de Carrare","zh":"卡拉拉大理石油画"},
  "olio su mattonella": {"en":"oil on tile","es":"óleo sobre azulejo","fr":"huile sur carreau","zh":"瓷砖油画"},
  "olio su tela e sabbia": {"en":"oil on canvas and sand","es":"óleo sobre lienzo y arena","fr":"huile sur toile et sable","zh":"布面与沙油画"},
  "olio su tela": {"en":"oil on canvas","es":"óleo sobre lienzo","fr":"huile sur toile","zh":"布面油画"},
  "olio su tyela": {"en":"oil on canvas","es":"óleo sobre lienzo","fr":"huile sur toile","zh":"布面油画"},

  "fotografo sconosciuto": {"en":"Unknown photographer","es":"Fotógrafo desconocido","fr":"Photographe inconnu","zh":"摄影师不详"},
  "tributo a": {"en":"Tribute to","es":"Homenaje a","fr":"Hommage à","zh":"致敬"},
  "tributo": {"en":"Tribute","es":"Homenaje","fr":"Hommage","zh":"致敬"},

  "verde marino": {"en":"sea green","es":"verde marino","fr":"vert marin","zh":"海绿色"},
  "arancione": {"en":"orange","es":"naranja","fr":"orange","zh":"橙色"},
  "celeste": {"en":"sky blue","es":"celeste","fr":"bleu ciel","zh":"天蓝色"},
  "giallo": {"en":"yellow","es":"amarillo","fr":"jaune","zh":"黄色"},
  "verde": {"en":"green","es":"verde","fr":"vert","zh":"绿色"},
  "rosso": {"en":"red","es":"rojo","fr":"rouge","zh":"红色"},
  "viola": {"en":"purple","es":"violeta","fr":"violet","zh":"紫色"},
  "bianco": {"en":"white","es":"blanco","fr":"blanc","zh":"白色"},
  "blue": {"en":"blue","es":"azul","fr":"bleu","zh":"蓝色"},
  "blu": {"en":"blue","es":"azul","fr":"bleu","zh":"蓝色"},
  "nero": {"en":"black","es":"negro","fr":"noir","zh":"黑色"},

  "anno 2020": {"en":"year 2020","es":"año 2020","fr":"année 2020","zh":"2020年"},
  "anno": {"en":"year","es":"año","fr":"année","zh":"年"},
  " su ": {"en":" on ","es":" sobre ","fr":" sur ","zh":" 于 "},
}

NAMES = {
  "steve mccurrydipinto":"Steve McCurry", "stevemccurry":"Steve McCurry", "steve mccurry":"Steve McCurry",
  "lee jeffriesdipinto":"Lee Jeffries", "lee jeffries":"Lee Jeffries",
  "mohammed muheisen":"Mohammed Muheisen", "mohamed muheisen":"Mohammed Muheisen", "mohammed muhesein":"Mohammed Muheisen",
  "hans silvester":"Hans Silvester", "thomas than":"Thomas Than", "emil leonoradi":"Emil Leonoradi",
  "betina la plante":"Betina La Plante", "nino bartuccio":"Nino Bartuccio", "jeri daking":"Jeri Daking",
  "carlo mari studio":"Carlo Mari Studio", "dimitry hoholo":"Dimitry Hoholo", "shirren lim":"Shirren Lim",
  "istvan kerekes":"Istvan Kerekes", "jean d'hugues":"Jean d'Hugues", "levent yavuz":"Levent Yavuz",
  "neven jurkovic":"Neven Jurkovic", "forsaken d sharon pruitt pink":"Forsaken (D. Sharon Pruitt Pink)",
  "nega projet":"NEGA PROJECT", "kazincbarcika":"Kazincbarcika",
}

ph_items = sorted(PH.items(), key=lambda kv: -len(kv[0]))
name_items = sorted(NAMES.items(), key=lambda kv: -len(kv[0]))

def tr(cap, lang):
    s = cap.lower().replace(".", " ").replace(",", " ")
    s = re.sub(r"\s+", " ", s).strip()
    tokens = []
    def sub(src, val):
        nonlocal s
        while src in s:
            key = f"\x00{len(tokens)}\x00"
            tokens.append(val)
            s = s.replace(src, key, 1)
    for it, trans in ph_items:
        sub(it, trans[lang])
    for it, proper in name_items:
        sub(it, proper)
    # leftover connectors
    for it, val in {" e ":{"en":" and ","es":" y ","fr":" et ","zh":" 和 "}}.items():
        s = s.replace(it, val[lang])
    for i, t in enumerate(tokens):
        s = s.replace(f"\x00{i}\x00", t)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,;:])", r"\1", s)
    return (s[:1].upper() + s[1:]) if s else s

# restructure series meta translations
meta = {
 "innocence-1": {
   "subtitle": {"it":"Serie I","en":"Series I","es":"Serie I","fr":"Série I","zh":"第一系列"},
   "year": {"it":"17 oli su tela","en":"17 oils on canvas","es":"17 óleos sobre lienzo","fr":"17 huiles sur toile","zh":"17幅布面油画"},
   "desc": {
     "it": d["opere"][0]["desc"],
     "en": "The debut series INNOCENCE I (17 oils on canvas) marks a turning point in Cortona's artistic research. Through a profound experimentation with primary colours and their visceral shades, an intense visual and emotional metamorphosis takes shape.\n\nFrom the partial framings of the early works, the artist's gaze gradually narrows until it \u201centers\u201d the subjects themselves, breaking down every distance: the space on the canvas shrinks to make room for the exploration of the Soul. An inner immersion that intensifies further in series II and III, turning painting into a pure journey through human emotional depth.",
     "es": "La serie de debut INNOCENCE I (17 oleos sobre lienzo) marca un punto de inflexion en la investigacion artistica de Cortona. A traves de una profunda experimentacion con los colores primarios y sus matices viscerales, toma forma una intensa metamorfosis visual y emocional.\n\nDesde los encuadres parciales de los inicios, la mirada de la artista se estrecha progresivamente hasta \u201centrar\u201d en los propios sujetos, derribando toda distancia: el espacio del lienzo se reduce para dar paso a la exploracion del Alma. Una inmersion interior que se intensifica aun mas en las series II y III, transformando la pintura en un puro viaje a traves de la profundidad emocional humana.",
     "fr": "La serie inaugurale INNOCENCE I (17 huiles sur toile) marque un tournant dans la recherche artistique de Cortona. A travers une profonde experimentation sur les couleurs primaires et leurs nuances viscerales, prend forme une intense metamorphose visuelle et emotionnelle.\n\nDes cadrages partiels des debuts, le regard de l'artiste se resserre progressivement jusqu'a \u201centrer\u201d dans les sujets eux-memes, abolissant toute distance : l'espace de la toile se reduit pour laisser place a l'exploration de l'Ame. Une immersion interieure qui s'intensifie encore dans les series II et III, transformant la peinture en un pur voyage a travers la profondeur emotionnelle humaine.",
     "zh": "首个系列《INNOCENCE I》（17幅布面油画）标志着Cortona艺术探索的重要转折。通过对原色及其深沉色调的深入实验，一场强烈的视觉与情感蜕变由此成形。\n\n从早期的局部构图，艺术家的目光逐渐收紧，直至\u201c进入\u201d对象本身，消弭一切距离：画布上的空间不断缩小，为灵魂的探索让出位置。这种内在的沉浸在第二与第三系列中愈发强烈，将绘画化为一场穿越人类情感深处的纯粹旅程。",
   },
 },
 "innocence-2": {
   "subtitle": {"it":"Serie II","en":"Series II","es":"Serie II","fr":"Série II","zh":"第二系列"},
   "year": {"it":"Olio e pigmenti fotoluminescenti su lamiera zincata","en":"Oil and photoluminescent pigments on galvanized sheet metal","es":"Óleo y pigmentos fotoluminiscentes sobre chapa galvanizada","fr":"Huile et pigments photoluminescents sur tôle galvanisée","zh":"镀锌金属板上的油彩与光致发光颜料"},
   "desc": {
     "it": d["opere"][1]["desc"],
     "en": "INNOCENCE \u2013 Series II is born from Cortona's research on inner light and the desire to give new life to the gaze of her subjects through art.\n\nThe works are made by hand on galvanized sheet metal with natural photoluminescent pigments that, once charged by light, glow in the dark revealing intense and surprising colours. Each painting is the result of a long artisanal process in which technique and sensitivity merge to create an ever-changing visual experience.\n\nLight becomes an integral part of the work, revealing what remains invisible and inviting the viewer on a journey toward the discovery of their own inner light.",
     "es": "INNOCENCE \u2013 Serie II nace de la investigacion de Cortona sobre la luz interior y el deseo de dar nueva vida a la mirada de sus sujetos a traves del arte.\n\nLas obras se realizan a mano sobre chapa galvanizada con pigmentos fotoluminiscentes naturales que, tras cargarse con la luz, se iluminan en la oscuridad revelando colores intensos y sorprendentes. Cada pintura es el resultado de un largo proceso artesanal en el que tecnica y sensibilidad se funden para crear una experiencia visual en continua transformacion.\n\nLa luz se convierte en parte integrante de la obra, revelando lo que permanece invisible e invitando al espectador a emprender un viaje hacia el descubrimiento de su propia luz interior.",
     "fr": "INNOCENCE \u2013 Serie II nait de la recherche de Cortona sur la lumiere interieure et du desir de redonner vie au regard de ses sujets par l'art.\n\nLes oeuvres sont realisees a la main sur tole galvanisee avec des pigments photoluminescents naturels qui, une fois charges par la lumiere, s'illuminent dans l'obscurite en revelant des couleurs intenses et surprenantes. Chaque tableau est le fruit d'un long processus artisanal ou technique et sensibilite se fondent pour creer une experience visuelle en perpetuelle transformation.\n\nLa lumiere devient partie integrante de l'oeuvre, revelant ce qui reste invisible et invitant le spectateur a un voyage vers la decouverte de sa propre lumiere interieure.",
     "zh": "《INNOCENCE 第二系列》源于Cortona对内在之光的探索，以及借由艺术赋予笔下人物目光新生命的渴望。\n\n作品在镀锌金属板上手工完成，采用天然光致发光颜料，经光照后能在黑暗中发光，显现出浓烈而惊艳的色彩。每一幅画都是漫长手工过程的结晶，技法与感性在其中交融，创造出不断变化的视觉体验。\n\n光成为作品不可分割的一部分，揭示隐匿之物，邀请观者踏上一段发现自身内在之光的旅程。",
   },
 },
 "innocence-3": {
   "subtitle": {"it":"Serie III","en":"Series III","es":"Serie III","fr":"Série III","zh":"第三系列"},
   "year": {"it":"10 oli su lamiera zincata \u2014 bianco e nero","en":"10 oils on galvanized sheet metal \u2014 black and white","es":"10 óleos sobre chapa galvanizada \u2014 blanco y negro","fr":"10 huiles sur tôle galvanisée \u2014 noir et blanc","zh":"10幅镀锌金属板油画 \u2014 黑白"},
   "desc": {
     "it": d["opere"][2]["desc"],
     "en": "INNOCENCE Series III is the final chapter of the series, composed of 10 oil paintings on galvanized sheet metal, all executed in black and white. Each sheet is prepared and worked by the artist with the same attention to detail and the same careful process.\n\nWith a deep passion for the contrast between light and shadow, Cortona brings this theme to the fore through the chiaroscuro of this series. The use of black and white allows the artist to explore the subtle emotional nuances of each gaze, creating a depth and intensity that captures the viewer's attention.\n\nThe result is a collection of works that explore the depth of the human soul through the powerful language of chiaroscuro.",
     "es": "INNOCENCE Serie III es el ultimo capitulo de la serie, compuesto por 10 pinturas al oleo sobre chapa galvanizada, todas ejecutadas en blanco y negro. Cada chapa es preparada y trabajada por la artista con la misma atencion al detalle y el mismo proceso cuidadoso.\n\nCon una profunda pasion por el contraste entre luz y sombra, Cortona hace emerger este tema a traves del claroscuro presente en esta serie. El uso del blanco y negro permite a la artista explorar los sutiles matices emocionales de cada mirada, creando una profundidad e intensidad que captura la atencion del espectador.\n\nEl resultado es una coleccion de obras que exploran la profundidad del alma humana a traves del poderoso lenguaje del claroscuro.",
     "fr": "INNOCENCE Serie III est le dernier chapitre de la serie, composee de 10 peintures a l'huile sur tole galvanisee, toutes executees en noir et blanc. Chaque tole est preparee et travaillee par l'artiste avec le meme souci du detail et le meme processus minutieux.\n\nAvec une profonde passion pour le contraste entre lumiere et ombre, Cortona fait emerger ce theme par le clair-obscur de cette serie. L'usage du noir et blanc permet a l'artiste d'explorer les subtiles nuances emotionnelles de chaque regard, creant une profondeur et une intensite qui captent l'attention du spectateur.\n\nLe resultat est une collection d'oeuvres qui explorent la profondeur de l'ame humaine a travers le puissant langage du clair-obscur.",
     "zh": "《INNOCENCE 第三系列》是该系列的最后篇章，由10幅镀锌金属板油画组成，全部以黑白呈现。每块金属板都由艺术家以同样的细致与严谨工序准备和处理。\n\nCortona对光与影的对比怀有深切热爱，并通过本系列的明暗对照法将这一主题凸显出来。黑白的运用让艺术家得以探索每一道目光中细微的情感层次，营造出摄人心魄的深度与张力。\n\n最终呈现的是一组以强烈的明暗语言探索人类灵魂深处的作品。",
   },
 },
 "maestri-di-marmo": {
   "subtitle": {"it":"Omaggio a Caravaggio e Michelangelo","en":"Homage to Caravaggio and Michelangelo","es":"Homenaje a Caravaggio y Miguel Ángel","fr":"Hommage à Caravage et Michel-Ange","zh":"向卡拉瓦乔与米开朗基罗致敬"},
   "year": {"it":"Olio su marmo di Carrara","en":"Oil on Carrara marble","es":"Óleo sobre mármol de Carrara","fr":"Huile sur marbre de Carrare","zh":"卡拉拉大理石油画"},
   "desc": {
     "it": d["opere"][3]["desc"],
     "en": "With Maestri di Marmo, Cortona pays homage to two giants of art history: Caravaggio and Michelangelo.\n\nMade on precious Carrara marble, the works reinterpret iconic details such as The Incredulity of Saint Thomas and The Creation of Adam, transforming them into a dialogue between tradition and contemporaneity.\n\nMarble, a symbol of eternity and beauty, becomes the ideal support to celebrate the expressive power of these masterpieces, offering the viewer a new perspective on their extraordinary artistic legacy.",
     "es": "Con Maestri di Marmo, Cortona rinde homenaje a dos gigantes de la historia del arte: Caravaggio y Miguel Angel.\n\nRealizadas sobre precioso marmol de Carrara, las obras reinterpretan detalles iconicos como La incredulidad de Santo Tomas y La creacion de Adan, transformandolos en un dialogo entre tradicion y contemporaneidad.\n\nEl marmol, simbolo de eternidad y belleza, se convierte en el soporte ideal para celebrar la fuerza expresiva de estas obras maestras, ofreciendo al espectador una nueva perspectiva sobre su extraordinario legado artistico.",
     "fr": "Avec Maestri di Marmo, Cortona rend hommage a deux geants de l'histoire de l'art : Caravage et Michel-Ange.\n\nRealisees sur du precieux marbre de Carrare, les oeuvres reinterpretent des details iconiques tels que L'incredulite de saint Thomas et La creation d'Adam, les transformant en un dialogue entre tradition et contemporaneite.\n\nLe marbre, symbole d'eternite et de beaute, devient le support ideal pour celebrer la force expressive de ces chefs-d'oeuvre, offrant au spectateur une nouvelle perspective sur leur extraordinaire heritage artistique.",
     "zh": "在《大理石大师》中，Cortona向艺术史上的两位巨匠致敬：卡拉瓦乔与米开朗基罗。\n\n作品以珍贵的卡拉拉大理石为材，重新诠释了《圣托马斯的怀疑》与《创造亚当》等标志性细节，将其转化为传统与当代之间的对话。\n\n大理石象征永恒与美，成为礼赞这些杰作表现力的理想载体，为观者提供了重新审视其非凡艺术遗产的全新视角。",
   },
 },
 "frammenti": {
   "subtitle": {"it":"Olio su mattonella","en":"Oil on tiles","es":"Óleo sobre azulejos","fr":"Huile sur carreaux","zh":"瓷砖油画"},
   "year": {"it":"2020","en":"2020","es":"2020","fr":"2020","zh":"2020"},
   "desc": {
     "it": d["opere"][4]["desc"],
     "en": "FRAMMENTI is a collection of oil paintings on tiles of various sizes, where each work represents an emotion, an instant, a part of human experience.\n\nEach tile is a fragment of a larger story: a dialogue between colour, matter and feeling that invites the viewer to recognise themselves in the infinite shades of the human soul.\n\nThe variety of formats creates a dynamic visual rhythm, turning each work into a piece of an emotional mosaic. Together, these fragments compose an intense and personal narrative about the complexity of emotions.",
     "es": "FRAMMENTI es una coleccion de pinturas al oleo sobre azulejos de distintos tamanos, donde cada obra representa una emocion, un instante, una parte de la experiencia humana.\n\nCada azulejo es un fragmento de un relato mas amplio: un dialogo entre color, materia y sentimiento que invita al espectador a reconocerse en los infinitos matices del alma humana.\n\nLa variedad de formatos crea un ritmo visual dinamico, transformando cada obra en una pieza de un mosaico emocional. Juntos, estos fragmentos componen una narracion intensa y personal sobre la complejidad de las emociones.",
     "fr": "FRAMMENTI est une collection de peintures a l'huile sur carreaux de differentes dimensions, ou chaque oeuvre represente une emotion, un instant, une part de l'experience humaine.\n\nChaque carreau est un fragment d'un recit plus vaste : un dialogue entre couleur, matiere et sentiment qui invite le spectateur a se reconnaitre dans les nuances infinies de l'ame humaine.\n\nLa variete des formats cree un rythme visuel dynamique, transformant chaque oeuvre en une piece d'une mosaique emotionnelle. Ensemble, ces fragments composent un recit intense et personnel sur la complexite des emotions.",
     "zh": "《碎片》是一组尺寸各异的瓷砖油画，每一件作品都代表一种情感、一个瞬间、人类经验的一部分。\n\n每块瓷砖都是更宏大叙事的碎片：色彩、物质与情感之间的对话，邀请观者在人类灵魂的无尽层次中认出自己。\n\n多样的画幅营造出富有动感的视觉节奏，使每件作品都成为情感马赛克中的一块。这些碎片汇聚成一段关于情感复杂性的强烈而私密的叙述。",
   },
 },
 "dopo-di-noi": {
   "subtitle": {"it":"Illustrazioni ispirate ai glifi astrologici","en":"Illustrations inspired by astrological glyphs","es":"Ilustraciones inspiradas en los glifos astrológicos","fr":"Illustrations inspirées des glyphes astrologiques","zh":"受占星符号启发的插画"},
   "year": {"it":"2024","en":"2024","es":"2024","fr":"2024","zh":"2024"},
   "desc": {
     "it": d["opere"][5]["desc"],
     "en": ".DOPO DI NOI. is the first project born from the collaboration between two sisters and two art forms: the painting of Cortona and the poetry of the writer Lie Larousse.\n\nFor the poetry collection published in 2024, Cortona created the cover and seven illustrations inspired by astrological glyphs, ancient symbols that hold universal and spiritual meanings.\n\nEach illustration accompanies a poem, becoming a visual message that invites reflection, inner growth and the rediscovery of the bond between the human being and the universe.",
     "es": ".DOPO DI NOI. es el primer proyecto nacido de la colaboracion entre dos hermanas y dos formas de arte: la pintura de Cortona y la poesia de la escritora Lie Larousse.\n\nPara el poemario publicado en 2024, Cortona realizo la portada y siete ilustraciones inspiradas en los glifos astrologicos, antiguos simbolos que encierran significados universales y espirituales.\n\nCada ilustracion acompana un poema, convirtiendose en un mensaje visual que invita a la reflexion, al crecimiento interior y al redescubrimiento del vinculo entre el ser humano y el universo.",
     "fr": ".DOPO DI NOI. est le premier projet ne de la collaboration entre deux soeurs et deux formes d'art : la peinture de Cortona et la poesie de l'ecrivaine Lie Larousse.\n\nPour le recueil de poemes publie en 2024, Cortona a realise la couverture et sept illustrations inspirees des glyphes astrologiques, symboles anciens porteurs de significations universelles et spirituelles.\n\nChaque illustration accompagne un poeme et devient un message visuel qui invite a la reflexion, a la croissance interieure et a la redecouverte du lien entre l'etre humain et l'univers.",
     "zh": "《DOPO DI NOI（我们之后）》是两姐妹与两种艺术形式合作诞生的首个项目：Cortona的绘画与作家Lie Larousse的诗歌。\n\n为2024年出版的诗集，Cortona创作了封面及七幅受占星符号启发的插画——这些古老的符号蕴含着普世而灵性的意义。\n\n每幅插画都伴随一首诗，化作一则视觉讯息，邀人反思、促进内在成长，并重新发现人与宇宙之间的联系。",
   },
 },
}

order = ["innocence-1","innocence-2","innocence-3","maestri-di-marmo","frammenti","dopo-di-noi"]
for i, slug in enumerate(order):
    o = d["opere"][i]
    m = meta[slug]
    o["subtitle"] = m["subtitle"]
    o["year"] = m["year"]
    o["desc"] = m["desc"]
    for im in o["images"]:
        it_cap = im["caption"]
        im["caption"] = {"it": it_cap, "en": tr(it_cap,"en"), "es": tr(it_cap,"es"), "fr": tr(it_cap,"fr"), "zh": tr(it_cap,"zh")}

json.dump(d, open("/app/frontend/src/data/content.json","w"), ensure_ascii=False, indent=2)

# print a few samples for review
import itertools
for o in d["opere"]:
    print("===", o["slug"])
    for im in o["images"][:2]:
        for lg in ["it","en","es","fr","zh"]:
            print(f"  [{lg}] {im['caption'][lg]}")
    break
print("DONE")
