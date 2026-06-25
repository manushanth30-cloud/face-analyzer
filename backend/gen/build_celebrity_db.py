#!/usr/bin/env python3
"""
Build celebrity_matcher.py with 1000 celebrity entries.
Run:  python gen/build_celebrity_db.py
"""
import hashlib, json, os, textwrap

CATS = [
    "Hollywood Actor","Hollywood Actress","Bollywood Actor","Bollywood Actress",
    "K-Pop / K-Drama","Musician","Athlete - Cricket","Athlete - Football",
    "Athlete - Other","TV Personality","Model","Historical / Iconic",
    "Tech / Business","South Indian",
]
SHAPES = ["Oval","Round","Square","Heart","Diamond","Oblong"]
KEYS = ["fr","sy","es","ct","np","lf","lr","jd","ck","fp","ft","gr"]
# Base vectors per shape: face_ratio, symmetry, eye_spacing, canthal_tilt,
#   nose_proportion, lip_fullness, lip_ratio, jaw_definition, cheekbone_height,
#   forehead_proportion, face_taper, golden_ratio
BASES = [
    [.54,.85,.50,.55,.48,.50,.46,.62,.65,.50,.55,.80],  # Oval
    [.62,.83,.50,.53,.50,.55,.46,.48,.55,.48,.38,.76],  # Round
    [.56,.84,.50,.54,.50,.50,.45,.80,.62,.50,.50,.80],  # Square
    [.52,.86,.52,.56,.46,.52,.46,.60,.68,.48,.62,.82],  # Heart
    [.50,.85,.52,.56,.46,.48,.46,.68,.75,.50,.62,.80],  # Diamond
    [.48,.83,.52,.55,.48,.50,.46,.68,.65,.55,.58,.78],  # Oblong
]

def make_vec(name, gender, si, ov):
    b = list(BASES[si])
    if gender == "M":
        b[0]+=.02; b[7]+=.04; b[8]-=.02; b[5]-=.02
    else:
        b[0]-=.01; b[5]+=.03; b[8]+=.03; b[3]+=.02
    oi = set()
    for k,v in ov.items():
        i = KEYS.index(k); b[i]=v; oi.add(i)
    h = hashlib.md5(name.encode()).hexdigest()
    for i in range(12):
        if i not in oi:
            n = (int(h[i*2:i*2+2],16)/255.0-0.5)*0.08
            b[i] = max(.05,min(.95,b[i]+n))
    return [round(v,2) for v in b]

# ── DATA: (name, gender, cat_idx, shape_idx, {overrides}, fun_fact) ──
D = [
# ═══ Hollywood Actors (120) ═══
("Brad Pitt","M",0,2,{"jd":.88,"sy":.91,"gr":.85},"Chiseled jawline icon"),
("Leonardo DiCaprio","M",0,1,{"fr":.63,"sy":.86},"Baby-faced blue eyes"),
("Chris Hemsworth","M",0,2,{"jd":.90,"ck":.75},"Thor-worthy square jaw"),
("Tom Cruise","M",0,0,{"sy":.93,"gr":.88},"Near-perfect symmetry"),
("Ryan Gosling","M",0,5,{"jd":.72,"gr":.81},"Brooding long face"),
("Denzel Washington","M",0,0,{"sy":.90,"gr":.86},"Commanding symmetry"),
("Will Smith","M",0,0,{"fr":.58,"lf":.62},"Megawatt wide smile"),
("George Clooney","M",0,0,{"sy":.90,"jd":.78},"Classic leading man"),
("Johnny Depp","M",0,0,{"ck":.76,"ct":.58},"High angular cheekbones"),
("Robert Downey Jr.","M",0,0,{"sy":.85,"es":.48},"Expressive brow arch"),
("Matt Damon","M",0,1,{"fr":.61,"jd":.58},"Boy-next-door face"),
("Ben Affleck","M",0,2,{"jd":.78,"fp":.56},"Prominent strong chin"),
("Christian Bale","M",0,4,{"ck":.78,"jd":.82},"Dramatic cheekbones"),
("Hugh Jackman","M",0,5,{"jd":.80,"fp":.56},"Elongated rugged face"),
("Jake Gyllenhaal","M",0,0,{"es":.56,"ct":.58},"Wide-set blue eyes"),
("Ryan Reynolds","M",0,3,{"jd":.72,"ft":.62},"Heart-shaped charmer"),
("Chris Evans","M",0,2,{"jd":.85,"sy":.89},"All-American jaw"),
("Chris Pratt","M",0,1,{"fr":.61,"jd":.58},"Softer round features"),
("Tom Hardy","M",0,2,{"jd":.82,"lf":.62},"Intense broad jaw"),
("Idris Elba","M",0,2,{"jd":.80,"sy":.88},"Broad powerful jaw"),
("Keanu Reeves","M",0,5,{"sy":.84,"ck":.66},"Ageless structure"),
("Morgan Freeman","M",0,1,{"fr":.59,"np":.55},"Warm rounded face"),
("Samuel L. Jackson","M",0,0,{"es":.56,"np":.54},"Wide-set fierce eyes"),
("Robert De Niro","M",0,5,{"jd":.72,"sy":.83},"Intense elongated face"),
("Al Pacino","M",0,5,{"ct":.56,"ck":.63},"Dark intense features"),
("Tom Hanks","M",0,1,{"fr":.59,"sy":.86},"Everyman warm face"),
("Harrison Ford","M",0,5,{"jd":.72,"sy":.82},"Rugged scar on chin"),
("Joaquin Phoenix","M",0,3,{"lf":.58,"sy":.80},"Distinctive lip scar"),
("Adam Driver","M",0,5,{"es":.58,"fr":.45},"Unconventional long face"),
("Oscar Isaac","M",0,0,{"sy":.87,"lf":.56},"Warm balanced face"),
("Michael B. Jordan","M",0,1,{"lf":.62,"sy":.89},"Full lips round face"),
("Chadwick Boseman","M",0,0,{"sy":.88,"ck":.72},"Regal oval structure"),
("Paul Rudd","M",0,0,{"sy":.85,"gr":.79},"Ageless proportions"),
("Mark Ruffalo","M",0,1,{"fr":.59,"jd":.55},"Friendly soft features"),
("Jeremy Renner","M",0,2,{"jd":.75,"ck":.62},"Sharp angular face"),
("Jason Momoa","M",0,2,{"jd":.82,"fr":.59},"Broad warrior jaw"),
("Henry Cavill","M",0,2,{"sy":.92,"jd":.90},"Superman jawline"),
("Benedict Cumberbatch","M",0,5,{"es":.58,"ck":.78},"Alien cheekbones"),
("Tom Hiddleston","M",0,5,{"sy":.86,"ck":.72},"Refined long face"),
("Eddie Redmayne","M",0,3,{"es":.56,"ct":.58},"Freckled striking face"),
("Daniel Craig","M",0,2,{"jd":.85,"sy":.86},"Blue-eyed bruiser jaw"),
("Matt Bomer","M",0,0,{"sy":.93,"gr":.90},"Near-perfect symmetry"),
("Zac Efron","M",0,2,{"jd":.80,"sy":.88},"Square-cut jaw"),
("Channing Tatum","M",0,2,{"jd":.78,"fr":.59},"Wide strong jaw"),
("Chris Pine","M",0,0,{"es":.56,"sy":.88},"Bright blue-eyed face"),
("Miles Teller","M",0,1,{"fr":.59,"jd":.62},"Relaxed round features"),
("Austin Butler","M",0,4,{"ck":.78,"ct":.58},"Sharp cheekbone angles"),
("Jamie Foxx","M",0,1,{"lf":.60,"sy":.86},"Warm expressive face"),
("Kevin Hart","M",0,1,{"fr":.61,"fp":.47},"Compact round face"),
("Dwayne Johnson","M",0,2,{"jd":.85,"fr":.63},"Massive square head"),
("Vin Diesel","M",0,1,{"fr":.63,"jd":.72},"Bald broad features"),
("Jason Statham","M",0,2,{"jd":.85,"sy":.85},"Bald rugged jaw"),
("Liam Neeson","M",0,5,{"fp":.58,"jd":.72},"Tall elongated face"),
("Russell Crowe","M",0,2,{"jd":.78,"fr":.59},"Rugged square face"),
("Javier Bardem","M",0,2,{"lf":.58,"jd":.78},"Brooding dark jaw"),
("Pedro Pascal","M",0,0,{"sy":.86,"lf":.56},"Warm approachable face"),
("Michael Fassbender","M",0,5,{"jd":.78,"ck":.72},"Angular elongated face"),
("James McAvoy","M",0,1,{"sy":.85,"es":.51},"Bright Scottish face"),
("Colin Farrell","M",0,0,{"ct":.57,"sy":.84},"Dark brooding eyes"),
("Dev Patel","M",0,5,{"ck":.70,"ct":.58},"Refined angular face"),
("Rami Malek","M",0,3,{"es":.61,"ct":.60},"Unusually wide-set eyes"),
("John Boyega","M",0,1,{"lf":.60,"fr":.61},"Full round face"),
("Mahershala Ali","M",0,0,{"sy":.88,"jd":.72},"Elegant proportions"),
("Jeff Goldblum","M",0,5,{"fr":.46,"es":.57},"Uniquely elongated face"),
("Willem Dafoe","M",0,5,{"ck":.72,"sy":.78},"Striking angular face"),
("Jude Law","M",0,0,{"sy":.88,"gr":.84},"Classic bone structure"),
("Ethan Hawke","M",0,0,{"sy":.83,"jd":.68},"Boyish proportions"),
("Matthew McConaughey","M",0,5,{"sy":.85,"jd":.72},"Relaxed long face"),
("Bradley Cooper","M",0,0,{"es":.56,"sy":.87},"Wide-set blue eyes"),
("Sam Rockwell","M",0,0,{"sy":.82,"jd":.65},"Versatile features"),
("Viggo Mortensen","M",0,5,{"jd":.72,"ck":.66},"Rugged lean face"),
("Clive Owen","M",0,2,{"jd":.80,"sy":.84},"Dark brooding jaw"),
("Daniel Kaluuya","M",0,1,{"es":.56,"sy":.87},"Expressive wide face"),
("Lakeith Stanfield","M",0,5,{"es":.56,"lf":.58},"Unique elongated face"),
("Jonathan Majors","M",0,2,{"jd":.82,"ck":.68},"Sculpted jawline"),
("Glen Powell","M",0,2,{"jd":.78,"sy":.87},"All-American jaw"),
("Barry Keoghan","M",0,3,{"sy":.80,"ft":.61},"Unconventional face"),
("Paul Mescal","M",0,1,{"sy":.84,"lf":.56},"Soft strong features"),
("Andrew Garfield","M",0,5,{"es":.53,"ck":.68},"Expressive long face"),
("Tobey Maguire","M",0,1,{"fr":.59,"sy":.84},"Youthful round face"),
("Orlando Bloom","M",0,0,{"sy":.86,"ck":.68},"Elfin refined face"),
("Elijah Wood","M",0,1,{"es":.58,"sy":.85},"Huge expressive eyes"),
("Ian McKellen","M",0,5,{"fp":.56,"sy":.82},"Distinguished long face"),
("Patrick Stewart","M",0,1,{"fp":.63,"jd":.72},"Commanding bald dome"),
("Anthony Hopkins","M",0,1,{"sy":.85,"jd":.68},"Penetrating stare"),
("Gary Oldman","M",0,0,{"sy":.83,"ck":.62},"Chameleon features"),
("Ralph Fiennes","M",0,5,{"ck":.70,"sy":.86},"Aristocratic bones"),
("Liam Hemsworth","M",0,2,{"jd":.82,"sy":.88},"Broad Australian jaw"),
("Dave Bautista","M",0,2,{"jd":.85,"fr":.63},"Massive broad skull"),
("Simu Liu","M",0,2,{"jd":.78,"sy":.87},"Clean angular jaw"),
("Henry Golding","M",0,0,{"sy":.89,"gr":.85},"Perfectly balanced face"),
("John Cho","M",0,0,{"sy":.86,"jd":.68},"Balanced clean face"),
("Steven Yeun","M",0,0,{"sy":.87,"ct":.57},"Warm natural face"),
("Kumail Nanjiani","M",0,0,{"jd":.68,"sy":.84},"Transformed features"),
("Riz Ahmed","M",0,5,{"ck":.68,"ct":.57},"Intense angular face"),
("Jesse Eisenberg","M",0,3,{"ft":.59,"sy":.82},"Narrow sharp face"),
("Robert Pattinson","M",0,4,{"ck":.80,"jd":.78},"Dramatic cheekbones"),
("Kit Harington","M",0,1,{"sy":.85,"jd":.68},"Dark curly-framed face"),
("Richard Madden","M",0,2,{"jd":.78,"sy":.87},"Scottish chiseled jaw"),
("Rege-Jean Page","M",0,0,{"sy":.90,"gr":.87},"Perfectly balanced face"),
("Jacob Elordi","M",0,5,{"fr":.45,"ft":.66},"Dramatically tall face"),
("Josh Brolin","M",0,2,{"jd":.85,"fr":.58},"Rugged heavy jaw"),
("Sean Penn","M",0,5,{"sy":.80,"jd":.72},"Weathered intense face"),
("Nicolas Cage","M",0,5,{"es":.53,"sy":.78},"Highly expressive face"),
("Sylvester Stallone","M",0,2,{"jd":.82,"sy":.78},"Asymmetric strong jaw"),
("Arnold Schwarzenegger","M",0,2,{"jd":.88,"fr":.62},"Massive Austrian jaw"),
("Bruce Willis","M",0,2,{"jd":.82,"fp":.56},"Hard bald structure"),
("Eddie Murphy","M",0,0,{"lf":.58,"sy":.85},"Wide bright smile"),
("Chiwetel Ejiofor","M",0,0,{"sy":.87,"ck":.68},"Elegant bone structure"),
("Forest Whitaker","M",0,1,{"sy":.78,"es":.53},"Distinctive eye droop"),
("Don Cheadle","M",0,4,{"ck":.72,"sy":.85},"Angular cheekbones"),
("Benicio del Toro","M",0,2,{"jd":.78,"sy":.80},"Rugged weathered jaw"),
("Michael Shannon","M",0,5,{"fp":.58,"fr":.46},"Towering intense face"),
("Casey Affleck","M",0,0,{"sy":.83,"jd":.65},"Understated features"),
("Timothee Chalamet","M",0,3,{"ck":.78,"ft":.66},"Razor-sharp cheekbones"),
("Tom Holland","M",0,1,{"fr":.58,"sy":.87},"Youthful round face"),
("Ezra Miller","M",0,4,{"ck":.75,"ct":.60},"Androgynous sharp face"),
("Mads Mikkelsen","M",0,5,{"ck":.75,"jd":.78},"Danish angular features"),
("Mark Wahlberg","M",0,2,{"jd":.78,"fr":.58},"Boston tough-guy jaw"),
("Will Ferrell","M",0,5,{"fp":.60,"fr":.48},"Tall comedic features"),
# ═══ Hollywood Actresses (120) ═══
("Angelina Jolie","F",1,2,{"lf":.85,"sy":.92,"gr":.90},"Legendary full lips"),
("Scarlett Johansson","F",1,3,{"lf":.72,"sy":.90},"Pillowy lips heart face"),
("Zendaya","F",1,0,{"ck":.75,"sy":.89},"Supermodel proportions"),
("Margot Robbie","F",1,3,{"sy":.91,"gr":.88},"Doll-like perfect face"),
("Emma Watson","F",1,3,{"ft":.60,"sy":.88},"Elfin refined features"),
("Emma Stone","F",1,1,{"es":.56,"sy":.87},"Huge expressive eyes"),
("Jennifer Lawrence","F",1,1,{"sy":.86,"fr":.59},"Girl-next-door face"),
("Natalie Portman","F",1,3,{"sy":.90,"gr":.87},"Petite perfect symmetry"),
("Cate Blanchett","F",1,0,{"ck":.75,"sy":.90},"Ethereal regal bones"),
("Nicole Kidman","F",1,5,{"sy":.88,"ck":.72},"Porcelain long face"),
("Charlize Theron","F",1,2,{"sy":.91,"ck":.78},"Supermodel jaw"),
("Halle Berry","F",1,0,{"sy":.90,"ck":.72},"Ageless balanced beauty"),
("Julia Roberts","F",1,5,{"lf":.70,"es":.56},"Iconic megawatt smile"),
("Sandra Bullock","F",1,0,{"sy":.87,"jd":.62},"Warm natural face"),
("Meryl Streep","F",1,5,{"sy":.85,"fp":.56},"Distinguished features"),
("Anne Hathaway","F",1,0,{"es":.58,"lf":.62},"Enormously expressive eyes"),
("Gal Gadot","F",1,0,{"sy":.91,"jd":.68},"Wonder Woman structure"),
("Lupita Nyong'o","F",1,0,{"ck":.75,"sy":.90},"Sculpted radiant face"),
("Viola Davis","F",1,1,{"lf":.60,"sy":.86},"Powerful expressive face"),
("Kerry Washington","F",1,0,{"sy":.88,"ck":.70},"Smooth porcelain oval"),
("Thandiwe Newton","F",1,3,{"ck":.72,"ct":.58},"High delicate cheekbones"),
("Zoe Saldana","F",1,3,{"ct":.60,"ck":.75},"Cat-like upturned eyes"),
("Jessica Alba","F",1,0,{"sy":.88,"gr":.84},"Warm symmetrical beauty"),
("Megan Fox","F",1,0,{"sy":.90,"lf":.62},"Striking blue eyes"),
("Olivia Wilde","F",1,2,{"es":.56,"jd":.68},"Sharp jaw wide eyes"),
("Brie Larson","F",1,1,{"sy":.86,"fr":.58},"Rounded approachable face"),
("Amy Adams","F",1,1,{"sy":.85,"fr":.58},"Soft luminous features"),
("Rachel McAdams","F",1,3,{"sy":.87,"ft":.60},"Classic heart face"),
("Blake Lively","F",1,0,{"sy":.88,"gr":.85},"California-perfect face"),
("Jennifer Aniston","F",1,0,{"sy":.87,"gr":.83},"Timelessly balanced face"),
("Reese Witherspoon","F",1,3,{"ft":.62,"jd":.58},"Pointed chin heart face"),
("Cameron Diaz","F",1,1,{"fr":.59,"lf":.55},"Sunny wide smile"),
("Drew Barrymore","F",1,1,{"fr":.61,"sy":.82},"Cherubic round features"),
("Penelope Cruz","F",1,0,{"lf":.62,"sy":.89},"Spanish dark-eyed beauty"),
("Salma Hayek","F",1,0,{"lf":.65,"ck":.68},"Lush full-featured beauty"),
("Sofia Vergara","F",1,0,{"lf":.62,"fr":.57},"Voluptuous warm features"),
("Jessica Chastain","F",1,0,{"sy":.87,"ck":.70},"Porcelain red-haired face"),
("Saoirse Ronan","F",1,1,{"es":.56,"sy":.86},"Wide-set ethereal eyes"),
("Anya Taylor-Joy","F",1,3,{"es":.65,"ct":.60},"Extraordinarily wide eyes"),
("Sydney Sweeney","F",1,1,{"sy":.87,"lf":.56},"Bright doe-eyed face"),
("Jenna Ortega","F",1,0,{"sy":.88,"jd":.62},"Petite precise features"),
("Hailee Steinfeld","F",1,0,{"sy":.87,"ck":.65},"Strong brow balanced face"),
("Dakota Johnson","F",1,0,{"sy":.86,"lf":.55},"Soft understated beauty"),
("Lily Collins","F",1,3,{"ct":.58,"sy":.88},"Iconic thick eyebrows"),
("Emilia Clarke","F",1,1,{"sy":.87,"lf":.56},"Warm wide bright smile"),
("Sophie Turner","F",1,0,{"sy":.86,"fp":.53},"Tall oval elegant face"),
("Ana de Armas","F",1,0,{"sy":.90,"lf":.58},"Luminous classic beauty"),
("Keira Knightley","F",1,2,{"jd":.72,"ck":.78},"Angular defined jaw"),
("Emily Blunt","F",1,0,{"sy":.88,"ck":.68},"Polished British face"),
("Tilda Swinton","F",1,5,{"ck":.75,"fp":.58},"Androgynous striking face"),
("Helena Bonham Carter","F",1,3,{"sy":.82,"ck":.68},"Quirky expressive face"),
("Kate Winslet","F",1,0,{"sy":.87,"lf":.55},"English rose beauty"),
("Naomi Watts","F",1,0,{"sy":.86,"ck":.68},"Refined understated face"),
("Gwyneth Paltrow","F",1,5,{"sy":.88,"ck":.70},"Elongated elegant bones"),
("Michelle Pfeiffer","F",1,3,{"sy":.90,"ck":.72},"Ageless feline features"),
("Sharon Stone","F",1,2,{"sy":.88,"jd":.72},"Ice-cool angular beauty"),
("Demi Moore","F",1,0,{"sy":.87,"lf":.55},"Striking dark features"),
("Winona Ryder","F",1,3,{"es":.56,"ct":.58},"Wide doe-eyed features"),
("Uma Thurman","F",1,5,{"es":.58,"ck":.68},"Statuesque wide-set eyes"),
("Sigourney Weaver","F",1,5,{"fp":.58,"jd":.65},"Tall commanding face"),
("Jodie Foster","F",1,0,{"sy":.86,"jd":.62},"Intelligent refined face"),
("Michelle Williams","F",1,1,{"sy":.85,"fr":.57},"Delicate round features"),
("Rooney Mara","F",1,3,{"ck":.72,"ft":.65},"Ethereal pale features"),
("Kristen Stewart","F",1,0,{"sy":.84,"jd":.62},"Cool androgynous beauty"),
("Amanda Seyfried","F",1,1,{"es":.58,"sy":.86},"Famously huge eyes"),
("Rachel Weisz","F",1,0,{"sy":.88,"lf":.55},"Classic dark-eyed beauty"),
("Cynthia Erivo","F",1,0,{"ck":.65,"sy":.87},"Powerful sculpted face"),
("Letitia Wright","F",1,0,{"sy":.86,"ck":.65},"Warm bright-eyed face"),
("Yara Shahidi","F",1,3,{"sy":.87,"ft":.60},"Youthful heart face"),
("Awkwafina","F",1,1,{"fr":.59,"sy":.82},"Distinctive character face"),
("Gemma Chan","F",1,0,{"sy":.89,"ck":.72},"Porcelain elegant face"),
("Constance Wu","F",1,1,{"sy":.86,"fr":.57},"Bright warm features"),
("Lucy Liu","F",1,4,{"ck":.75,"ct":.58},"Sharp diamond features"),
("Sandra Oh","F",1,1,{"sy":.85,"lf":.55},"Warm expressive roundness"),
("Vanessa Hudgens","F",1,0,{"lf":.58,"sy":.86},"Exotic warm beauty"),
("Lily James","F",1,0,{"sy":.87,"ck":.68},"Classic English beauty"),
("Daisy Ridley","F",1,1,{"sy":.86,"fr":.57},"Bright expressive face"),
("Felicity Jones","F",1,3,{"sy":.86,"ft":.60},"Delicate heart face"),
("Alicia Vikander","F",1,0,{"sy":.88,"ct":.58},"Scandinavian refined face"),
("Rebecca Ferguson","F",1,0,{"sy":.88,"jd":.62},"Swedish strong features"),
("Eva Green","F",1,5,{"lf":.58,"ct":.58},"Smoldering dark intensity"),
("Marion Cotillard","F",1,0,{"sy":.89,"lf":.58},"French classic face"),
("Lea Seydoux","F",1,1,{"sy":.87,"lf":.58},"Soft French beauty"),
("Diane Kruger","F",1,0,{"sy":.88,"ck":.72},"German angular beauty"),
("Helen Mirren","F",1,0,{"sy":.85,"jd":.62},"Distinguished regal face"),
("Judi Dench","F",1,1,{"sy":.84,"fp":.51},"Commanding petite face"),
("Whoopi Goldberg","F",1,1,{"fr":.61,"np":.56},"Distinctive broad face"),
("Queen Latifah","F",1,1,{"fr":.62,"lf":.62},"Regal rounded features"),
("Octavia Spencer","F",1,1,{"fr":.61,"lf":.58},"Warm inviting features"),
("Taraji P. Henson","F",1,0,{"ck":.65,"lf":.58},"High cheekbone beauty"),
("Regina King","F",1,0,{"sy":.87,"ck":.68},"Elegant defined features"),
("Danai Gurira","F",1,0,{"jd":.65,"ck":.68},"Warrior regal bones"),
("Tessa Thompson","F",1,0,{"sy":.87,"ck":.68},"Refined versatile face"),
("Zazie Beetz","F",1,3,{"es":.56,"ck":.68},"Delicate mixed features"),
("Jodie Comer","F",1,0,{"sy":.88,"gr":.84},"Chameleon English beauty"),
("Phoebe Waller-Bridge","F",1,5,{"sy":.84,"fp":.56},"Elongated witty features"),
("Olivia Colman","F",1,1,{"sy":.84,"fr":.58},"Warm approachable face"),
("Emma Thompson","F",1,5,{"sy":.84,"fp":.56},"Tall elegant British face"),
("Rachel Brosnahan","F",1,3,{"sy":.87,"ft":.60},"Vintage-styled beauty"),
("Maya Hawke","F",1,0,{"es":.56,"sy":.85},"Inherited striking face"),
("Millie Bobby Brown","F",1,1,{"sy":.87,"fr":.57},"Youthful evolving face"),
("Dove Cameron","F",1,3,{"sy":.88,"lf":.58},"Doll-like symmetry"),
("Kiernan Shipka","F",1,3,{"sy":.86,"ft":.60},"Petite refined features"),
("Joey King","F",1,1,{"sy":.85,"fr":.59},"Round youthful face"),
("Thomasin McKenzie","F",1,3,{"sy":.86,"ft":.60},"Delicate NZ beauty"),
("Selena Gomez","F",1,1,{"sy":.86,"fr":.59},"Youthful round features"),
("Florence Pugh","F",1,1,{"sy":.86,"jd":.58},"Fiercely rounded face"),
("Elizabeth Olsen","F",1,2,{"sy":.88,"ck":.70},"Strong wide cheekbones"),
("Aubrey Plaza","F",1,0,{"sy":.85,"ct":.58},"Dark sardonic beauty"),
("Sarah Paulson","F",1,0,{"sy":.85,"ck":.65},"Versatile expressive face"),
("Kate Beckinsale","F",1,0,{"sy":.89,"gr":.85},"Timeless English beauty"),
("Monica Bellucci","F",1,0,{"lf":.65,"sy":.90},"Italian goddess features"),
("Zhang Ziyi","F",1,0,{"sy":.89,"ck":.72},"Porcelain Chinese beauty"),
("Fan Bingbing","F",1,0,{"sy":.90,"gr":.87},"Flawless porcelain skin"),
("Jessica Biel","F",1,2,{"jd":.68,"sy":.87},"Athletic angular face"),
("Kerry Condon","F",1,3,{"sy":.86,"ft":.60},"Irish delicate features"),
("Carey Mulligan","F",1,1,{"sy":.85,"fr":.57},"Soft English rose face"),
("Jurnee Smollett","F",1,0,{"sy":.87,"ck":.68},"Luminous warm features"),
("Amandla Stenberg","F",1,3,{"es":.56,"sy":.86},"Wide-eyed youthful face"),
("Daisy Edgar-Jones","F",1,3,{"sy":.87,"ft":.60},"Normal People delicate"),
# ═══ Bollywood Actors (70) ═══
("Shah Rukh Khan","M",2,0,{"sy":.87,"gr":.82},"King of dimpled charm"),
("Hrithik Roshan","M",2,0,{"sy":.92,"gr":.90},"Greek god of Bollywood"),
("Ranveer Singh","M",2,2,{"jd":.78,"lf":.56},"Wildly expressive face"),
("Ranbir Kapoor","M",2,0,{"sy":.88,"lf":.52},"Soft romantic features"),
("Salman Khan","M",2,2,{"jd":.82,"fr":.59},"Muscular broad jaw"),
("Aamir Khan","M",2,1,{"sy":.86,"jd":.62},"Perfectionist precise face"),
("Akshay Kumar","M",2,2,{"jd":.78,"sy":.85},"Athletic angular jaw"),
("Amitabh Bachchan","M",2,5,{"fp":.58,"ck":.70},"Towering elongated face"),
("Shahid Kapoor","M",2,0,{"sy":.88,"lf":.55},"Chocolate boy features"),
("Varun Dhawan","M",2,2,{"jd":.75,"sy":.86},"Boyish sharp jaw"),
("Tiger Shroff","M",2,0,{"sy":.87,"jd":.72},"Action hero proportions"),
("Kartik Aaryan","M",2,0,{"sy":.86,"ck":.65},"Charming dimpled cheeks"),
("Vicky Kaushal","M",2,2,{"jd":.78,"sy":.86},"Intense defined jaw"),
("Ayushmann Khurrana","M",2,0,{"sy":.85,"lf":.52},"Relatable warm face"),
("Rajkummar Rao","M",2,0,{"sy":.84,"jd":.62},"Understated refined face"),
("Sushant Singh Rajput","M",2,4,{"ck":.72,"sy":.87},"Dimpled angular face"),
("Irrfan Khan","M",2,5,{"es":.56,"ck":.65},"Soulful deep-set eyes"),
("Nawazuddin Siddiqui","M",2,0,{"sy":.80,"np":.51},"Intense raw features"),
("Anil Kapoor","M",2,0,{"sy":.84,"lf":.55},"Ageless jhakaas face"),
("Saif Ali Khan","M",2,5,{"jd":.72,"sy":.86},"Royal elongated face"),
("Arjun Kapoor","M",2,2,{"jd":.78,"fr":.59},"Broad strong jawline"),
("Siddharth Malhotra","M",2,2,{"jd":.78,"sy":.87},"Chiseled model jawline"),
("Aditya Roy Kapur","M",2,0,{"sy":.86,"ck":.68},"Tall dreamy features"),
("Farhan Akhtar","M",2,5,{"sy":.84,"jd":.68},"Athletic elongated face"),
("John Abraham","M",2,2,{"jd":.82,"fr":.59},"Bodybuilder sharp jaw"),
("Abhishek Bachchan","M",2,5,{"fp":.56,"sy":.84},"Tall inherited features"),
("Arjun Rampal","M",2,2,{"jd":.80,"ck":.72},"Model-actor jawline"),
("Sonu Sood","M",2,2,{"jd":.80,"fr":.57},"Tall chiseled features"),
("Pankaj Tripathi","M",2,1,{"fr":.59,"sy":.82},"Everyman natural face"),
("Manoj Bajpayee","M",2,0,{"sy":.83,"es":.51},"Intense expressive eyes"),
("Vikrant Massey","M",2,0,{"sy":.84,"jd":.62},"Subtle relatable face"),
("R. Madhavan","M",2,0,{"sy":.86,"lf":.55},"Dimpled romantic face"),
("Diljit Dosanjh","M",2,1,{"sy":.85,"lf":.56},"Warm Punjabi features"),
("Randeep Hooda","M",2,5,{"jd":.75,"sy":.84},"Rugged intense face"),
("Vidyut Jammwal","M",2,2,{"jd":.80,"sy":.86},"Chiseled action body jaw"),
("Rohit Saraf","M",2,0,{"sy":.86,"fr":.55},"Fresh youthful face"),
("Ishaan Khatter","M",2,0,{"sy":.85,"ct":.57},"Expressive lively face"),
("Riteish Deshmukh","M",2,0,{"sy":.83,"lf":.52},"Versatile natural face"),
("Emraan Hashmi","M",2,0,{"sy":.84,"ct":.56},"Serial kisser dimples"),
("Sanjay Dutt","M",2,2,{"jd":.82,"fr":.60},"Brawny tough-guy jaw"),
("Govinda","M",2,1,{"fr":.60,"sy":.83},"Comedy king round face"),
("Dharmendra","M",2,0,{"sy":.86,"jd":.72},"He-man of Hindi cinema"),
("Sunny Deol","M",2,2,{"jd":.82,"fr":.60},"Powerful broad jaw"),
("Bobby Deol","M",2,0,{"sy":.85,"jd":.68},"Transformed chiseled face"),
("Jackie Shroff","M",2,5,{"sy":.83,"jd":.72},"Rugged elongated face"),
("Suniel Shetty","M",2,2,{"jd":.80,"sy":.84},"Athletic angular jaw"),
("Abhay Deol","M",2,0,{"sy":.85,"ck":.65},"Indie refined features"),
("Ali Fazal","M",2,0,{"sy":.85,"lf":.55},"Warm hazel-eyed face"),
("Rajesh Khanna","M",2,0,{"sy":.85,"lf":.55},"Iconic dimpled cheeks"),
("Dev Anand","M",2,0,{"sy":.87,"gr":.83},"Evergreen puff-haired face"),
("Dilip Kumar","M",2,0,{"sy":.86,"gr":.82},"Tragedy king features"),
("Naseeruddin Shah","M",2,5,{"sy":.84,"es":.53},"Intense piercing gaze"),
("Anupam Kher","M",2,1,{"fp":.60,"sy":.83},"Versatile bald features"),
("Boman Irani","M",2,0,{"sy":.84,"fp":.55},"Expressive Parsi features"),
("Paresh Rawal","M",2,1,{"sy":.82,"jd":.58},"Comedic versatile face"),
("Kay Kay Menon","M",2,0,{"sy":.83,"es":.52},"Intense deep-set eyes"),
("Jimmy Shergill","M",2,0,{"sy":.84,"jd":.68},"Gentle Punjabi features"),
("Sharman Joshi","M",2,0,{"sy":.83,"fr":.55},"Everyday relatable face"),
("Vivek Oberoi","M",2,0,{"sy":.84,"ck":.65},"Sharp refined features"),
("Divyenndu","M",2,0,{"sy":.82,"lf":.52},"Quirky Munna features"),
("Jitendra Kumar","M",2,1,{"fr":.58,"sy":.83},"Relatable round face"),
("Pratik Gandhi","M",2,0,{"sy":.84,"jd":.65},"Chameleon precise face"),
("Jim Sarbh","M",2,5,{"ck":.68,"sy":.85},"Angular refined features"),
("Vijay Varma","M",2,0,{"sy":.85,"ct":.57},"Intense watchful eyes"),
("Adarsh Gourav","M",2,3,{"sy":.84,"ft":.60},"Sharp youthful face"),
("Gulshan Grover","M",2,2,{"jd":.75,"sy":.82},"Bad man menacing jaw"),
("Mithun Chakraborty","M",2,1,{"sy":.84,"lf":.55},"Disco dancer round face"),
("Vinod Khanna","M",2,0,{"sy":.87,"jd":.72},"Classic 70s leading man"),
("Fardeen Khan","M",2,0,{"sy":.85,"ck":.65},"Refined star-son face"),
("Rajeev Khandelwal","M",2,0,{"sy":.84,"jd":.68},"TV-to-film sharp face"),
# ═══ Bollywood Actresses (80) ═══
("Deepika Padukone","F",3,0,{"sy":.91,"ck":.75},"Statuesque golden ratio"),
("Aishwarya Rai","F",3,0,{"sy":.93,"gr":.92},"Most beautiful face ever"),
("Priyanka Chopra","F",3,0,{"sy":.89,"jd":.65},"Miss World jawline"),
("Alia Bhatt","F",3,3,{"sy":.87,"ft":.62},"Petite heart-shaped face"),
("Katrina Kaif","F",3,0,{"sy":.90,"gr":.87},"Symmetrical mixed beauty"),
("Kareena Kapoor Khan","F",3,0,{"sy":.89,"ck":.72},"Begum royal features"),
("Madhuri Dixit","F",3,1,{"sy":.88,"lf":.60},"Iconic dimpled smile"),
("Kajol","F",3,0,{"sy":.86,"es":.56},"Unibrow wide-eyed beauty"),
("Rani Mukerji","F",3,1,{"sy":.86,"es":.55},"Expressive bright eyes"),
("Anushka Sharma","F",3,3,{"sy":.88,"ft":.60},"Dimpled heart face"),
("Shraddha Kapoor","F",3,3,{"sy":.87,"lf":.55},"Doe-eyed delicate face"),
("Kriti Sanon","F",3,0,{"sy":.88,"ck":.68},"Tall model proportions"),
("Janhvi Kapoor","F",3,3,{"sy":.87,"lf":.58},"Ethereal soft features"),
("Sara Ali Khan","F",3,1,{"sy":.86,"lf":.55},"Royal dimpled cheeks"),
("Kiara Advani","F",3,0,{"sy":.88,"gr":.85},"Radiant balanced face"),
("Disha Patani","F",3,0,{"sy":.87,"lf":.58},"Doll-like features"),
("Nora Fatehi","F",3,0,{"sy":.87,"lf":.62},"Exotic proportions"),
("Jacqueline Fernandez","F",3,0,{"sy":.87,"lf":.58},"Sri Lankan bright face"),
("Sonam Kapoor","F",3,5,{"sy":.87,"ck":.72},"High fashion features"),
("Kangana Ranaut","F",3,0,{"sy":.86,"ck":.70},"Fierce regal face"),
("Vidya Balan","F",3,1,{"sy":.85,"lf":.58},"Expressive warm face"),
("Tabu","F",3,0,{"sy":.88,"ck":.70},"Ageless enigmatic beauty"),
("Rekha","F",3,0,{"sy":.87,"lf":.62},"Eternal glamour queen"),
("Sridevi","F",3,0,{"sy":.89,"es":.55},"Thunder eyes legendary"),
("Hema Malini","F",3,0,{"sy":.88,"gr":.84},"Dream girl proportions"),
("Juhi Chawla","F",3,3,{"sy":.86,"lf":.55},"Dimpled heart beauty"),
("Raveena Tandon","F",3,0,{"sy":.87,"lf":.58},"Tip tip barsa beauty"),
("Karisma Kapoor","F",3,0,{"sy":.87,"ck":.68},"Lolo refined features"),
("Sushmita Sen","F",3,0,{"sy":.90,"gr":.87},"Miss Universe structure"),
("Preity Zinta","F",3,3,{"sy":.87,"lf":.55},"Dimpled vivacious face"),
("Taapsee Pannu","F",3,0,{"sy":.86,"jd":.62},"Athletic strong face"),
("Bhumi Pednekar","F",3,1,{"sy":.85,"lf":.55},"Natural earthy beauty"),
("Yami Gautam","F",3,3,{"sy":.87,"ck":.68},"Himalayan fair beauty"),
("Radhika Madan","F",3,0,{"sy":.86,"ct":.58},"Perky natural face"),
("Sanya Malhotra","F",3,1,{"sy":.85,"fr":.58},"Girl-next-door charm"),
("Fatima Sana Shaikh","F",3,0,{"sy":.86,"ck":.68},"Dangal strong face"),
("Radhika Apte","F",3,0,{"sy":.85,"ct":.58},"Indie elegant face"),
("Sobhita Dhulipala","F",3,0,{"sy":.88,"ck":.72},"Architectural beauty"),
("Mrunal Thakur","F",3,0,{"sy":.87,"lf":.58},"Luminous warm face"),
("Triptii Dimri","F",3,3,{"sy":.87,"lf":.56},"National crush face"),
("Ananya Panday","F",3,3,{"sy":.86,"ft":.60},"Youthful heart face"),
("Wamiqa Gabbi","F",3,3,{"sy":.86,"ct":.58},"Bright petite features"),
("Sharvari Wagh","F",3,0,{"sy":.87,"ck":.68},"Fresh elegant face"),
("Manushi Chhillar","F",3,0,{"sy":.89,"gr":.86},"Miss World structure"),
("Aditi Rao Hydari","F",3,0,{"sy":.89,"ck":.72},"Ethereal Nawabi beauty"),
("Dia Mirza","F",3,0,{"sy":.88,"gr":.84},"Eco-beauty proportions"),
("Lara Dutta","F",3,0,{"sy":.88,"jd":.62},"Miss Universe jaw"),
("Lisa Haydon","F",3,5,{"sy":.87,"ck":.70},"Supermodel long face"),
("Kalki Koechlin","F",3,5,{"sy":.85,"es":.56},"French-Indian features"),
("Richa Chadha","F",3,0,{"sy":.85,"lf":.56},"Expressive indie face"),
("Nimrat Kaur","F",3,0,{"sy":.86,"ck":.68},"Refined Punjabi face"),
("Huma Qureshi","F",3,1,{"sy":.85,"lf":.58},"Warm rounded beauty"),
("Sonakshi Sinha","F",3,1,{"sy":.85,"jd":.60},"Dabangg strong face"),
("Parineeti Chopra","F",3,1,{"sy":.85,"lf":.55},"Dimpled bubbly face"),
("Chitrangda Singh","F",3,0,{"sy":.88,"ck":.72},"Sultry defined features"),
("Genelia Deshmukh","F",3,3,{"sy":.87,"ft":.60},"Cute heart-shaped face"),
("Bipasha Basu","F",3,0,{"sy":.87,"lf":.60},"Dusky fitness beauty"),
("Shilpa Shetty","F",3,0,{"sy":.88,"ck":.70},"Yoga-sculpted features"),
("Bhagyashree","F",3,0,{"sy":.86,"lf":.52},"Maine Pyar Kiya face"),
("Madhubala","F",3,0,{"sy":.90,"gr":.88},"Venus of Indian cinema"),
("Meenakshi Seshadri","F",3,0,{"sy":.87,"ck":.68},"Classic dance features"),
("Neena Gupta","F",3,0,{"sy":.85,"jd":.60},"Ageless bold features"),
("Shabana Azmi","F",3,5,{"sy":.85,"ck":.68},"Intense dramatic face"),
("Dimple Kapadia","F",3,3,{"sy":.87,"lf":.58},"Bobby dimpled charm"),
("Zeenat Aman","F",3,0,{"sy":.88,"gr":.84},"Iconic 70s glamour face"),
("Mouni Roy","F",3,0,{"sy":.87,"ck":.70},"TV-to-film beauty"),
("Kriti Kharbanda","F",3,0,{"sy":.86,"lf":.56},"Bright cheerful face"),
("Urvashi Rautela","F",3,0,{"sy":.88,"gr":.85},"Miss Universe runner-up"),
("Urmila Matondkar","F",3,0,{"sy":.87,"lf":.58},"Rangeela expressive face"),
("Nargis Fakhri","F",3,0,{"sy":.87,"ck":.68},"American-Pak mixed face"),
("Neha Sharma","F",3,0,{"sy":.86,"ck":.68},"Bright Bollywood beauty"),
("Amrita Rao","F",3,3,{"sy":.86,"ft":.60},"Vivah cute heart face"),
("Mallika Sherawat","F",3,0,{"sy":.86,"lf":.62},"Bold screen siren face"),
("Twinkle Khanna","F",3,0,{"sy":.86,"ck":.68},"Author star-wife face"),
("Neha Dhupia","F",3,0,{"sy":.86,"jd":.62},"Roadies anchor beauty"),
("Ameesha Patel","F",3,0,{"sy":.86,"lf":.55},"Gadar heroine face"),
("Mithila Palkar","F",3,3,{"sy":.86,"ft":.58},"Digital-age cute face"),
("Konkona Sen Sharma","F",3,0,{"sy":.85,"ck":.65},"Indie cinema face"),
("Tillotama Shome","F",3,0,{"sy":.85,"ck":.65},"Art film refined face"),
("Swara Bhasker","F",3,0,{"sy":.85,"lf":.56},"Outspoken indie beauty"),
# ═══ K-Pop / K-Drama (80) ═══
("Kim Taehyung","M",4,0,{"sy":.92,"gr":.89},"Perfect V-shaped face"),
("Jungkook","M",4,0,{"sy":.91,"ck":.70},"Doe-eyed golden ratio"),
("Jimin","M",4,3,{"sy":.90,"ft":.64},"Delicate feline features"),
("RM","M",4,4,{"ck":.72,"sy":.86},"Strong dimpled cheekbones"),
("Suga","M",4,0,{"sy":.88,"fr":.53},"Cat-like narrow face"),
("Jin","M",4,0,{"sy":.92,"gr":.90},"Worldwide handsome face"),
("J-Hope","M",4,3,{"sy":.87,"ck":.70},"Heart jaw sunshine face"),
("G-Dragon","M",4,4,{"ck":.75,"sy":.87},"Fashion-icon angular face"),
("T.O.P","M",4,2,{"jd":.78,"sy":.87},"Deep-voiced square jaw"),
("Taeyang","M",4,0,{"sy":.88,"jd":.68},"Sculpted singer face"),
("Song Joong-ki","M",4,0,{"sy":.90,"gr":.86},"Captain Yoo sharp face"),
("Park Seo-joon","M",4,2,{"jd":.78,"sy":.89},"Itaewon Class jaw"),
("Lee Min-ho","M",4,5,{"sy":.90,"gr":.87},"Hallyu king long face"),
("Hyun Bin","M",4,0,{"sy":.91,"jd":.72},"Captain Ri chiseled face"),
("Park Bo-gum","M",4,0,{"sy":.90,"gr":.86},"Nation's boyfriend face"),
("Ji Chang-wook","M",4,0,{"sy":.89,"jd":.72},"Action hero jawline"),
("Nam Joo-hyuk","M",4,5,{"sy":.87,"ck":.68},"Tall model features"),
("Lee Jong-suk","M",4,5,{"sy":.88,"ck":.70},"Sharp elongated features"),
("Kim Soo-hyun","M",4,0,{"sy":.90,"gr":.86},"My Love tear-duct mole"),
("Gong Yoo","M",4,0,{"sy":.89,"jd":.72},"Goblin ahjussi charm"),
("Lee Dong-wook","M",4,0,{"sy":.89,"ck":.72},"Grim Reaper sharp face"),
("Cha Eun-woo","M",4,0,{"sy":.93,"gr":.91},"Face genius symmetry"),
("Seo In-guk","M",4,1,{"sy":.87,"lf":.55},"Reply 1997 warm face"),
("Park Hyung-sik","M",4,0,{"sy":.89,"jd":.68},"Strong flower boy face"),
("Choi Woo-shik","M",4,1,{"sy":.86,"fr":.58},"Parasite friendly face"),
("Kim Woo-bin","M",4,5,{"sy":.87,"jd":.72},"Model-actor strong jaw"),
("Lee Joon-gi","M",4,3,{"sy":.88,"ft":.62},"Moon Lovers angular face"),
("Jung Hae-in","M",4,0,{"sy":.89,"gr":.85},"Boyfriend material face"),
("Wi Ha-joon","M",4,2,{"jd":.78,"sy":.88},"Squid Game sharp jaw"),
("Hwang In-youp","M",4,0,{"sy":.88,"ck":.70},"True Beauty tall face"),
("Song Kang","M",4,0,{"sy":.89,"gr":.86},"Sweet Home doe eyes"),
("Ahn Bo-hyun","M",4,2,{"jd":.80,"sy":.87},"Military jaw definition"),
("Lee Do-hyun","M",4,0,{"sy":.88,"ck":.68},"Youth of May face"),
("Byeon Woo-seok","M",4,5,{"sy":.88,"ck":.70},"Lovely Runner tall face"),
("Yeo Jin-goo","M",4,1,{"sy":.87,"fr":.57},"Child-actor grown face"),
("Baekhyun","M",4,3,{"sy":.89,"ft":.62},"EXO puppy-eyed face"),
("Sehun","M",4,0,{"sy":.90,"jd":.72},"EXO sharp jawline"),
("Kai","M",4,0,{"sy":.89,"ck":.70},"EXO dance god face"),
("Bang Chan","M",4,2,{"jd":.78,"sy":.88},"Stray Kids leader jaw"),
("Jackson Wang","M",4,2,{"jd":.78,"sy":.87},"GOT7 athletic jaw"),
("Jennie Kim","F",4,4,{"ck":.75,"sy":.90},"Cat-eyed BLACKPINK face"),
("Lisa Manobal","F",4,0,{"sy":.90,"ck":.72},"Thai-born doll face"),
("Jisoo Kim","F",4,1,{"sy":.90,"gr":.87},"Classic Korean beauty"),
("Rose Park","F",4,3,{"sy":.89,"ft":.62},"Slim elegant features"),
("IU","F",4,3,{"sy":.89,"gr":.86},"Nation's little sister"),
("Bae Suzy","F",4,0,{"sy":.90,"gr":.87},"Nation's first love face"),
("Song Hye-kyo","F",4,1,{"sy":.90,"gr":.87},"Hallyu queen round face"),
("Jun Ji-hyun","F",4,0,{"sy":.89,"ck":.72},"My Love sharp face"),
("Han So-hee","F",4,3,{"sy":.90,"ck":.72},"My Name fierce beauty"),
("Kim Yoo-jung","F",4,1,{"sy":.89,"gr":.86},"Child-star grown beauty"),
("Park Shin-hye","F",4,0,{"sy":.89,"gr":.85},"Heirs soft beauty"),
("Kim Tae-ri","F",4,0,{"sy":.88,"ck":.70},"Twenty-Five angular face"),
("Bae Doona","F",4,0,{"sy":.87,"ct":.58},"Indie auteur beauty"),
("Han Hyo-joo","F",4,0,{"sy":.89,"lf":.56},"Bright luminous face"),
("Moon Ga-young","F",4,3,{"sy":.88,"ft":.60},"True Beauty heart face"),
("Shin Min-a","F",4,0,{"sy":.89,"lf":.55},"Hometown Cha-Cha face"),
("Son Ye-jin","F",4,0,{"sy":.90,"gr":.87},"CLOY elegant beauty"),
("Park Min-young","F",4,0,{"sy":.89,"ck":.70},"Secretary Kim beauty"),
("Kim Ji-won","F",4,3,{"sy":.88,"ft":.62},"Descendants sharp face"),
("Lim Ji-yeon","F",4,0,{"sy":.88,"ck":.70},"The Glory fierce face"),
("Tzuyu","F",4,0,{"sy":.91,"gr":.88},"TWICE most beautiful"),
("Nayeon","F",4,3,{"sy":.89,"lf":.58},"TWICE bunny-teeth charm"),
("Karina","F",4,0,{"sy":.91,"gr":.89},"aespa AI-like perfection"),
("Winter","F",4,3,{"sy":.89,"ft":.62},"aespa cat-like features"),
("Irene","F",4,0,{"sy":.92,"gr":.90},"Red Velvet face genius"),
("Joy","F",4,1,{"sy":.88,"lf":.58},"Red Velvet sunny face"),
("Yuna","F",4,0,{"sy":.89,"ck":.70},"ITZY tall model face"),
("Miyeon","F",4,0,{"sy":.89,"gr":.86},"I-DLE classic beauty"),
("Minji","F",4,0,{"sy":.90,"gr":.87},"NewJeans fresh face"),
("Hanni","F",4,3,{"sy":.89,"ft":.60},"NewJeans Viet-Aus beauty"),
("Kazuha","F",4,0,{"sy":.89,"gr":.86},"LE SSERAFIM ballet face"),
("Sakura","F",4,3,{"sy":.88,"ft":.60},"LE SSERAFIM J-pop face"),
("Wonyoung","F",4,0,{"sy":.91,"gr":.89},"IVE living doll face"),
("Yujin","F",4,0,{"sy":.89,"gr":.86},"IVE MC bright face"),
("Kim So-hyun","F",4,3,{"sy":.88,"ft":.60},"Child-star refined face"),
("Go Min-si","F",4,0,{"sy":.87,"ck":.68},"Sweet Home strong face"),
("Kim Da-mi","F",4,0,{"sy":.87,"ct":.58},"Itaewon unique beauty"),
("Jeon Yeo-been","F",4,0,{"sy":.88,"ck":.70},"Vincenzo elegant face"),
("Lee Sung-kyung","F",4,5,{"sy":.88,"ck":.70},"Model-actress long face"),
("Shin Hye-sun","F",4,0,{"sy":.88,"ck":.68},"Mr Queen versatile face"),
# ═══ Musicians (100) ═══
("Beyonce","F",5,0,{"sy":.91,"gr":.88},"Queen Bey golden ratio"),
("Taylor Swift","F",5,0,{"sy":.88,"ck":.68},"All-American sweetheart"),
("Rihanna","F",5,0,{"sy":.90,"ck":.75},"Barbadian sculpted face"),
("Harry Styles","M",5,2,{"jd":.78,"sy":.88},"Dimpled rock-star jaw"),
("The Weeknd","M",5,0,{"sy":.86,"lf":.58},"Moody dark features"),
("Dua Lipa","F",5,0,{"sy":.89,"ck":.72},"Albanian supermodel face"),
("Ariana Grande","F",5,3,{"sy":.87,"ft":.62},"Petite doe-eyed heart"),
("Billie Eilish","F",5,1,{"sy":.86,"es":.56},"Wide-eyed round face"),
("Ed Sheeran","M",5,1,{"fr":.61,"sy":.82},"Red-haired round face"),
("Adele","F",5,1,{"sy":.86,"lf":.58},"Soulful rounded features"),
("Drake","M",5,0,{"sy":.86,"lf":.58},"Bearded oval profile"),
("Post Malone","M",5,1,{"sy":.80,"np":.52},"Tattooed round face"),
("Justin Bieber","M",5,0,{"sy":.87,"jd":.68},"Pop prince sharp jaw"),
("Shawn Mendes","M",5,2,{"jd":.78,"sy":.88},"Canadian chiseled jaw"),
("Bruno Mars","M",5,1,{"sy":.87,"lf":.58},"Compact expressive face"),
("Lady Gaga","F",5,0,{"sy":.87,"ck":.70},"Italian angular beauty"),
("Katy Perry","F",5,1,{"sy":.86,"lf":.58},"Wide-eyed pop face"),
("Nicki Minaj","F",5,3,{"lf":.68,"sy":.86},"Bold full-lipped face"),
("Cardi B","F",5,3,{"lf":.65,"sy":.85},"Bronx bold features"),
("Megan Thee Stallion","F",5,0,{"sy":.87,"jd":.65},"Hot girl strong face"),
("SZA","F",5,0,{"sy":.87,"ck":.70},"Ethereal R&B beauty"),
("Doja Cat","F",5,3,{"sy":.87,"ck":.72},"Chameleon sharp face"),
("Lizzo","F",5,1,{"lf":.62,"sy":.85},"Radiant full face"),
("Bad Bunny","M",5,1,{"sy":.84,"fr":.60},"Round reggaeton face"),
("Rosalia","F",5,0,{"sy":.88,"ck":.72},"Spanish flamenco beauty"),
("Shakira","F",5,0,{"sy":.88,"ck":.70},"Colombian golden face"),
("Camila Cabello","F",5,0,{"sy":.87,"lf":.58},"Cuban warm beauty"),
("Olivia Rodrigo","F",5,0,{"sy":.87,"ck":.68},"Gen-Z bright face"),
("Sabrina Carpenter","F",5,3,{"sy":.87,"ft":.60},"Petite heart face"),
("Miley Cyrus","F",5,3,{"sy":.86,"jd":.62},"Evolved edgy features"),
("Lana Del Rey","F",5,0,{"lf":.62,"sy":.86},"Vintage full-lipped face"),
("Halsey","F",5,3,{"sy":.86,"ck":.70},"Androgynous sharp face"),
("Zayn Malik","M",5,0,{"sy":.90,"gr":.87},"Chiseled Bradford face"),
("Niall Horan","M",5,1,{"sy":.85,"fr":.59},"Irish round friendly face"),
("Louis Tomlinson","M",5,2,{"jd":.75,"sy":.85},"Sharp jawline singer"),
("Travis Scott","M",5,0,{"sy":.84,"lf":.58},"Braided dark features"),
("A$AP Rocky","M",5,0,{"sy":.86,"ck":.68},"Fashion icon cheekbones"),
("Tyler the Creator","M",5,1,{"sy":.84,"fr":.60},"Creative round face"),
("Pharrell Williams","M",5,0,{"sy":.87,"gr":.82},"Ageless smooth face"),
("Kanye West","M",5,2,{"jd":.72,"sy":.84},"Strong broad jawline"),
("Jay-Z","M",5,0,{"sy":.84,"lf":.60},"Mogul strong features"),
("Eminem","M",5,2,{"jd":.75,"sy":.84},"Detroit sharp jaw"),
("Snoop Dogg","M",5,5,{"fr":.46,"sy":.83},"Iconic elongated face"),
("Kendrick Lamar","M",5,0,{"sy":.85,"fr":.55},"Compact intense face"),
("J. Cole","M",5,0,{"sy":.85,"ck":.65},"Thoughtful balanced face"),
("Jack Harlow","M",5,1,{"sy":.84,"fr":.59},"Curly-haired round face"),
("Lil Nas X","M",5,0,{"sy":.86,"ck":.68},"Bold bright features"),
("Frank Ocean","M",5,0,{"sy":.86,"ck":.68},"Enigmatic smooth face"),
("Troye Sivan","M",5,3,{"sy":.87,"ft":.62},"Androgynous sharp face"),
("Charlie Puth","M",5,0,{"sy":.86,"jd":.68},"Eyebrow-slit charm"),
("John Legend","M",5,1,{"sy":.87,"lf":.58},"Smooth rounded face"),
("Usher","M",5,0,{"sy":.88,"jd":.70},"Sculpted R&B face"),
("Chris Brown","M",5,0,{"sy":.86,"lf":.58},"Dimpled R&B features"),
("Adam Levine","M",5,0,{"sy":.87,"jd":.72},"Tattooed sharp face"),
("Freddie Mercury","M",5,5,{"sy":.82,"lf":.55},"Iconic overbite profile"),
("David Bowie","M",5,4,{"ck":.75,"sy":.84},"Alien diamond face"),
("Prince","M",5,3,{"sy":.86,"ft":.62},"Androgynous beauty icon"),
("Michael Jackson","M",5,4,{"sy":.87,"ck":.78},"Changed diamond face"),
("Whitney Houston","F",5,0,{"sy":.88,"ck":.70},"Radiant diva beauty"),
("Amy Winehouse","F",5,3,{"sy":.84,"lf":.58},"Retro beehive framed"),
("Madonna","F",5,0,{"sy":.86,"jd":.62},"Material Girl evolution"),
("Cher","F",5,0,{"sy":.86,"ck":.72},"Ageless iconic features"),
("Celine Dion","F",5,5,{"sy":.86,"ck":.70},"Angular elongated face"),
("Mariah Carey","F",5,0,{"sy":.87,"lf":.58},"Butterfly beauty face"),
("Janet Jackson","F",5,0,{"sy":.87,"ck":.68},"Sculpted Jackson face"),
("Alicia Keys","F",5,0,{"sy":.88,"ck":.70},"No-makeup natural beauty"),
("Tina Turner","F",5,0,{"sy":.86,"ck":.70},"Fierce lioness features"),
("Stevie Wonder","M",5,1,{"sy":.83,"fr":.60},"Soulful rounded face"),
("Bob Marley","M",5,0,{"sy":.84,"ck":.65},"Rasta framed features"),
("Jimi Hendrix","M",5,0,{"sy":.84,"ck":.68},"Afro-framed sharp face"),
("Kurt Cobain","M",5,5,{"sy":.82,"es":.55},"Grunge blue-eyed face"),
("Mick Jagger","M",5,5,{"lf":.70,"fr":.46},"Iconic enormous lips"),
("John Lennon","M",5,1,{"sy":.84,"fr":.58},"Round bespectacled face"),
("Paul McCartney","M",5,0,{"sy":.86,"gr":.82},"Beatle baby face"),
("Elton John","M",5,1,{"sy":.83,"fp":.55},"Spectacled round face"),
("Gwen Stefani","F",5,0,{"sy":.87,"ck":.70},"Platinum pop beauty"),
("Christina Aguilera","F",5,0,{"sy":.87,"lf":.60},"Powerful pipes face"),
("Pink","F",5,3,{"sy":.86,"jd":.62},"Edgy athletic face"),
("Sia","F",5,0,{"sy":.85,"fp":.55},"Wig-hidden mystery face"),
("Lorde","F",5,0,{"sy":.86,"ck":.68},"Kiwi dark beauty"),
("Charli XCX","F",5,0,{"sy":.86,"ck":.68},"Brat pop angular face"),
("FKA Twigs","F",5,0,{"sy":.87,"ck":.72},"Avant-garde beauty"),
("Janelle Monae","F",5,0,{"sy":.88,"ck":.70},"Android elegant face"),
("H.E.R.","F",5,0,{"sy":.86,"ck":.68},"Shades-hidden mystery"),
("Khalid","M",5,1,{"sy":.85,"fr":.60},"Smooth R&B round face"),
("Sam Smith","M",5,1,{"sy":.85,"fr":.60},"Non-binary pop face"),
("Jason Derulo","M",5,0,{"sy":.87,"jd":.72},"Talk Dirty sharp jaw"),
("Bono","M",5,0,{"sy":.84,"fp":.55},"U2 shades iconic face"),
("Bruce Springsteen","M",5,2,{"jd":.75,"sy":.84},"Boss blue-collar jaw"),
("Dave Grohl","M",5,5,{"sy":.83,"jd":.68},"Foo Fighters beard face"),
("Avril Lavigne","F",5,3,{"sy":.86,"ft":.60},"Sk8er punk heart face"),
("Fergie","F",5,0,{"sy":.86,"ck":.68},"Fergalicious sharp face"),
("Mary J. Blige","F",5,0,{"sy":.86,"ck":.70},"Queen of hip-hop face"),
("Alanis Morissette","F",5,0,{"sy":.85,"ck":.68},"Jagged Little face"),
("Grimes","F",5,3,{"sy":.85,"ft":.62},"Ethereal elf features"),
("21 Savage","M",5,0,{"sy":.84,"jd":.70},"Cross tattoo forehead"),
("Ice Spice","F",5,1,{"sy":.86,"ck":.68},"Bronx curly-haired icon"),
("Demi Lovato","F",5,1,{"sy":.86,"lf":.58},"Strong vocal power face"),
("J Balvin","M",5,1,{"sy":.84,"fr":.59},"Reggaeton color hair"),
("Liam Payne","M",5,0,{"sy":.86,"jd":.72},"1D heartthrob jawline"),
# ═══ Athletes - Cricket (60) ═══
("Virat Kohli","M",6,0,{"sy":.88,"jd":.75},"King Kohli sharp beard"),
("MS Dhoni","M",6,1,{"sy":.86,"jd":.68},"Captain Cool round face"),
("Sachin Tendulkar","M",6,1,{"sy":.85,"fr":.59},"Master Blaster face"),
("Rohit Sharma","M",6,1,{"sy":.85,"fr":.60},"Hitman round face"),
("Babar Azam","M",6,0,{"sy":.88,"gr":.85},"Pakistani prince face"),
("Kane Williamson","M",6,0,{"sy":.86,"jd":.68},"Kiwi captain beard"),
("Pat Cummins","M",6,2,{"jd":.78,"sy":.87},"Aussie captain jaw"),
("Ben Stokes","M",6,2,{"jd":.78,"fr":.59},"English warrior jaw"),
("Joe Root","M",6,0,{"sy":.86,"fr":.55},"Yorkshire baby face"),
("Steve Smith","M",6,0,{"sy":.84,"jd":.65},"Unorthodox long face"),
("David Warner","M",6,2,{"jd":.78,"fr":.58},"Bull-terrier jaw"),
("KL Rahul","M",6,0,{"sy":.87,"jd":.72},"Stylish sharp features"),
("Rishabh Pant","M",6,1,{"sy":.84,"fr":.60},"Boyish round face"),
("Jasprit Bumrah","M",6,0,{"sy":.85,"jd":.68},"Intense action face"),
("Ravindra Jadeja","M",6,0,{"sy":.85,"jd":.70},"Sir Jadeja sword face"),
("Hardik Pandya","M",6,2,{"jd":.78,"sy":.86},"Athletic sharp jaw"),
("Shubman Gill","M",6,0,{"sy":.88,"gr":.85},"Prince of cricket face"),
("Suryakumar Yadav","M",6,0,{"sy":.85,"lf":.55},"Mr 360 warm face"),
("Ravichandran Ashwin","M",6,0,{"sy":.84,"fp":.55},"Brainy bowler face"),
("Mohammed Shami","M",6,2,{"jd":.75,"sy":.85},"Bearded pacer face"),
("Yuzvendra Chahal","M",6,5,{"fr":.46,"sy":.83},"Slim spinner face"),
("Shreyas Iyer","M",6,0,{"sy":.86,"jd":.68},"Curly-haired captain"),
("Yashasvi Jaiswal","M",6,0,{"sy":.86,"jd":.68},"Young gun sharp face"),
("Shaheen Shah Afridi","M",6,5,{"jd":.75,"sy":.86},"Tall fast bowler face"),
("Mohammad Rizwan","M",6,0,{"sy":.85,"jd":.68},"Keeper warrior face"),
("Fakhar Zaman","M",6,2,{"jd":.78,"sy":.85},"Aggressive opener jaw"),
("Rashid Khan","M",6,0,{"sy":.85,"fr":.55},"Afghan spin prodigy"),
("Shakib Al Hasan","M",6,0,{"sy":.84,"jd":.68},"Bangladesh all-rounder"),
("Quinton de Kock","M",6,1,{"sy":.84,"fr":.59},"SA keeper round face"),
("Kagiso Rabada","M",6,0,{"sy":.85,"jd":.70},"SA pacer intense face"),
("AB de Villiers","M",6,0,{"sy":.87,"gr":.84},"Mr 360 balanced face"),
("Faf du Plessis","M",6,2,{"jd":.78,"sy":.86},"SA captain sharp jaw"),
("Trent Boult","M",6,5,{"sy":.84,"fr":.48},"NZ left-arm long face"),
("Mitchell Starc","M",6,5,{"jd":.75,"sy":.85},"Aussie pacer tall face"),
("Travis Head","M",6,2,{"jd":.75,"sy":.85},"Aussie batter jaw"),
("Marnus Labuschagne","M",6,0,{"sy":.85,"fp":.55},"SA-born Aussie face"),
("Jos Buttler","M",6,0,{"sy":.86,"jd":.68},"English skipper face"),
("Jonny Bairstow","M",6,1,{"sy":.84,"fr":.59},"Red-haired round face"),
("Stuart Broad","M",6,5,{"jd":.72,"sy":.84},"Tall English bowler"),
("James Anderson","M",6,5,{"sy":.84,"jd":.68},"Swing king long face"),
("Jason Holder","M",6,5,{"jd":.72,"sy":.84},"Windies giant face"),
("Nicholas Pooran","M",6,0,{"sy":.85,"lf":.56},"T20 dynamite face"),
("Shimron Hetmyer","M",6,1,{"sy":.84,"fr":.59},"Windies explosive face"),
("Sunil Narine","M",6,0,{"sy":.84,"jd":.65},"Mystery spinner face"),
("Andre Russell","M",6,2,{"jd":.80,"fr":.60},"Muscle Russell jaw"),
("Chris Gayle","M",6,2,{"jd":.78,"fr":.61},"Universe Boss jaw"),
("Kumar Sangakkara","M",6,0,{"sy":.87,"gr":.84},"Sri Lankan classic face"),
("Lasith Malinga","M",6,1,{"sy":.83,"fr":.59},"Slinger wild-hair face"),
("Brian Lara","M",6,0,{"sy":.86,"ck":.65},"Prince of Trinidad"),
("Ricky Ponting","M",6,2,{"jd":.78,"sy":.85},"Aussie captain jaw"),
("Glenn McGrath","M",6,5,{"jd":.72,"fr":.48},"Pigeon tall face"),
("Adam Gilchrist","M",6,0,{"sy":.86,"jd":.68},"Gilchrist keeper face"),
("Jacques Kallis","M",6,2,{"jd":.78,"fr":.58},"SA all-rounder jaw"),
("Wasim Akram","M",6,0,{"sy":.85,"jd":.68},"Sultan of swing face"),
("Muttiah Muralitharan","M",6,1,{"sy":.82,"fr":.59},"Spin wizard face"),
("Ruturaj Gaikwad","M",6,0,{"sy":.85,"jd":.68},"CSK prince face"),
("Ishan Kishan","M",6,1,{"sy":.84,"fr":.58},"Young keeper face"),
("Tim Southee","M",6,0,{"sy":.85,"jd":.68},"NZ swing bowler face"),
("Ross Taylor","M",6,0,{"sy":.85,"np":.52},"NZ batting legend face"),
("Josh Hazlewood","M",6,5,{"jd":.72,"sy":.84},"Tall Aussie pacer face"),
# ═══ Athletes - Football (50) ═══
("Cristiano Ronaldo","M",7,2,{"sy":.91,"jd":.85},"Perfect symmetry icon"),
("Lionel Messi","M",7,1,{"sy":.87,"fr":.58},"GOAT compact face"),
("Neymar","M",7,0,{"sy":.87,"ck":.68},"Brazilian flair face"),
("Kylian Mbappe","M",7,0,{"sy":.88,"jd":.72},"French speed face"),
("David Beckham","M",7,0,{"sy":.90,"gr":.87},"Golden Balls symmetry"),
("Zinedine Zidane","M",7,1,{"sy":.86,"fp":.58},"Bald maestro dome"),
("Ronaldinho","M",7,1,{"sy":.83,"lf":.62},"Buck-toothed smile icon"),
("Thierry Henry","M",7,0,{"sy":.87,"jd":.72},"French striker face"),
("Wayne Rooney","M",7,1,{"sy":.83,"fr":.60},"English bulldog face"),
("Sergio Ramos","M",7,2,{"jd":.82,"sy":.87},"Spanish warrior jaw"),
("Gerard Pique","M",7,2,{"jd":.80,"sy":.87},"Catalonian strong jaw"),
("Luka Modric","M",7,5,{"sy":.86,"fr":.48},"Croatian maestro face"),
("Robert Lewandowski","M",7,2,{"jd":.78,"sy":.87},"Polish striker jaw"),
("Erling Haaland","M",7,2,{"jd":.82,"fr":.60},"Viking massive jaw"),
("Jude Bellingham","M",7,0,{"sy":.88,"jd":.72},"English prince face"),
("Mohamed Salah","M",7,0,{"sy":.86,"lf":.55},"Egyptian king curls"),
("Virgil van Dijk","M",7,2,{"jd":.82,"fr":.60},"Dutch giant jaw"),
("Kevin De Bruyne","M",7,1,{"sy":.86,"fr":.58},"Belgian ginger face"),
("Antoine Griezmann","M",7,0,{"sy":.86,"jd":.68},"French forward face"),
("Karim Benzema","M",7,0,{"sy":.86,"jd":.72},"Real Madrid striker"),
("Zlatan Ibrahimovic","M",7,5,{"jd":.78,"fr":.48},"Swedish god nose"),
("Paolo Maldini","M",7,0,{"sy":.89,"gr":.86},"Italian elegance icon"),
("Ronaldo Nazario","M",7,1,{"sy":.85,"fr":.60},"Brazilian phenomenon"),
("Pele","M",7,1,{"sy":.85,"fr":.59},"King of football face"),
("Diego Maradona","M",7,1,{"sy":.83,"fr":.60},"Argentine legend face"),
("Gareth Bale","M",7,0,{"sy":.86,"jd":.72},"Welsh golf-loving face"),
("Son Heung-min","M",7,0,{"sy":.88,"gr":.85},"Korean Tottenham star"),
("Pedri","M",7,0,{"sy":.87,"fr":.55},"Spanish prodigy face"),
("Vinicius Jr.","M",7,0,{"sy":.87,"ck":.68},"Brazilian flair face"),
("Phil Foden","M",7,1,{"sy":.86,"fr":.58},"Stockport Iniesta face"),
("Bukayo Saka","M",7,0,{"sy":.87,"lf":.56},"Starboy bright face"),
("Marcus Rashford","M",7,0,{"sy":.87,"jd":.72},"Manchester forward face"),
("Harry Kane","M",7,0,{"sy":.86,"jd":.72},"England captain face"),
("Gianluigi Buffon","M",7,2,{"jd":.80,"sy":.87},"Italian keeper jaw"),
("Steven Gerrard","M",7,2,{"jd":.78,"sy":.85},"Liverpool captain jaw"),
("Frank Lampard","M",7,0,{"sy":.85,"fp":.55},"Chelsea super brain"),
("Andres Iniesta","M",7,1,{"sy":.86,"fr":.57},"Spanish maestro face"),
("Xavi Hernandez","M",7,1,{"sy":.86,"fp":.56},"Barca brain face"),
("Paul Pogba","M",7,0,{"sy":.86,"jd":.72},"French flair mohawk"),
("Eden Hazard","M",7,1,{"sy":.86,"fr":.59},"Belgian dribbler face"),
("Lamine Yamal","M",7,0,{"sy":.87,"fr":.55},"Spanish prodigy teen"),
("Florian Wirtz","M",7,0,{"sy":.87,"fr":.55},"German wonderkid face"),
("Marco van Basten","M",7,0,{"sy":.87,"jd":.72},"Dutch striker legend"),
("Johan Cruyff","M",7,5,{"sy":.86,"ck":.68},"Total football face"),
("Franz Beckenbauer","M",7,0,{"sy":.86,"jd":.72},"Kaiser elegant face"),
("George Best","M",7,0,{"sy":.86,"ck":.68},"Belfast boy icon"),
("Bobby Charlton","M",7,1,{"sy":.84,"fp":.58},"England 66 hero face"),
("Sadio Mane","M",7,0,{"sy":.86,"jd":.68},"Senegalese warrior face"),
("Gianluigi Donnarumma","M",7,2,{"jd":.78,"fr":.60},"Giant keeper face"),
("Alphonso Davies","M",7,0,{"sy":.86,"lf":.56},"Canadian speedster face"),
# ═══ Athletes - Other (40) ═══
("Serena Williams","F",8,2,{"jd":.68,"sy":.87},"Powerhouse athletic face"),
("Roger Federer","M",8,0,{"sy":.89,"gr":.86},"Elegance personified"),
("LeBron James","M",8,2,{"jd":.80,"fr":.60},"King James broad jaw"),
("Michael Jordan","M",8,1,{"sy":.87,"jd":.72},"GOAT determined face"),
("Rafael Nadal","M",8,2,{"jd":.80,"sy":.86},"Bull of Manacor jaw"),
("Novak Djokovic","M",8,0,{"sy":.87,"jd":.72},"Serbian precision face"),
("Venus Williams","F",8,0,{"sy":.86,"ck":.68},"Tennis queen features"),
("Naomi Osaka","F",8,1,{"sy":.86,"fr":.58},"Japanese Haitian face"),
("Maria Sharapova","F",8,0,{"sy":.89,"ck":.72},"Russian model beauty"),
("Usain Bolt","M",8,0,{"sy":.86,"jd":.72},"Lightning Bolt smile"),
("Michael Phelps","M",8,5,{"sy":.85,"fr":.48},"Swimmer elongated face"),
("Kobe Bryant","M",8,2,{"jd":.78,"sy":.87},"Mamba sharp jaw"),
("Stephen Curry","M",8,0,{"sy":.87,"fr":.55},"Baby-faced assassin"),
("Kevin Durant","M",8,5,{"sy":.85,"fr":.47},"Slim Reaper long face"),
("Shaquille O'Neal","M",8,2,{"jd":.80,"fr":.63},"Diesel massive head"),
("Tiger Woods","M",8,0,{"sy":.87,"jd":.68},"Focused intense face"),
("Ronda Rousey","F",8,2,{"jd":.72,"sy":.86},"MMA warrior jaw"),
("Conor McGregor","M",8,2,{"jd":.80,"sy":.85},"Notorious sharp jaw"),
("Floyd Mayweather","M",8,0,{"sy":.86,"jd":.70},"Pretty Boy face"),
("Manny Pacquiao","M",8,1,{"sy":.85,"fr":.58},"Pacman compact face"),
("Mike Tyson","M",8,2,{"jd":.82,"fr":.62},"Iron Mike massive jaw"),
("Muhammad Ali","M",8,0,{"sy":.88,"gr":.84},"Greatest face of boxing"),
("Simone Biles","F",8,1,{"sy":.87,"fr":.58},"GOAT gymnast face"),
("Mary Kom","F",8,1,{"sy":.85,"jd":.62},"Magnificent Mary face"),
("PV Sindhu","F",8,0,{"sy":.86,"ck":.68},"Shuttler tall face"),
("Neeraj Chopra","M",8,0,{"sy":.87,"jd":.75},"Golden javelin face"),
("Lewis Hamilton","M",8,0,{"sy":.87,"jd":.72},"F1 GOAT sharp face"),
("Max Verstappen","M",8,2,{"jd":.78,"sy":.86},"Dutch F1 champion jaw"),
("Tom Brady","M",8,2,{"jd":.80,"sy":.88},"NFL GOAT strong jaw"),
("Wayne Gretzky","M",8,0,{"sy":.85,"jd":.68},"Great One hockey face"),
("Lindsey Vonn","F",8,0,{"sy":.87,"jd":.65},"Alpine beauty face"),
("Carl Lewis","M",8,0,{"sy":.86,"jd":.68},"Sprint king features"),
("Andre Agassi","M",8,1,{"sy":.85,"fr":.58},"Tennis rebel face"),
("Pete Sampras","M",8,0,{"sy":.86,"jd":.72},"Pistol Pete face"),
("Yao Ming","M",8,5,{"fr":.48,"sy":.85},"Giant center long face"),
("Giannis Antetokounmpo","M",8,0,{"sy":.86,"jd":.72},"Greek Freak face"),
("Anna Kournikova","F",8,0,{"sy":.89,"gr":.86},"Tennis pin-up beauty"),
("Nadia Comaneci","F",8,0,{"sy":.87,"ck":.68},"Perfect 10 face"),
("Jackie Joyner-Kersee","F",8,0,{"sy":.86,"jd":.65},"Track legend face"),
("Danica Patrick","F",8,0,{"sy":.86,"ck":.68},"Racing beauty face"),
# ═══ TV Personalities (60) ═══
("Bryan Cranston","M",9,5,{"jd":.72,"sy":.85},"Heisenberg bald face"),
("Aaron Paul","M",9,0,{"sy":.85,"jd":.68},"Jesse Pinkman sharp face"),
("Jon Hamm","M",9,2,{"jd":.82,"sy":.88},"Don Draper jaw icon"),
("Elisabeth Moss","F",9,1,{"sy":.85,"es":.55},"Handmaid expressive eyes"),
("Bob Odenkirk","M",9,0,{"sy":.83,"jd":.65},"Saul Goodman features"),
("Steve Carell","M",9,0,{"sy":.84,"jd":.65},"Michael Scott face"),
("John Krasinski","M",9,2,{"jd":.78,"sy":.87},"Jim Halpert sharp jaw"),
("Jenna Fischer","F",9,3,{"sy":.86,"ft":.60},"Pam Beesly heart face"),
("Rainn Wilson","M",9,1,{"sy":.82,"fp":.58},"Dwight tall forehead"),
("Mindy Kaling","F",9,1,{"sy":.85,"fr":.59},"Kelly bright face"),
("Jim Parsons","M",9,5,{"sy":.84,"fr":.48},"Sheldon elongated face"),
("Kaley Cuoco","F",9,3,{"sy":.87,"lf":.55},"Penny blonde heart face"),
("Maitreyi Ramakrishnan","F",9,0,{"sy":.86,"ck":.68},"Devi Tamil beauty"),
("Penn Badgley","M",9,0,{"sy":.86,"jd":.68},"You stalker curly face"),
("Victoria Pedretti","F",9,3,{"sy":.87,"ck":.70},"Haunting ethereal face"),
("Jason Bateman","M",9,0,{"sy":.85,"jd":.68},"Ozark dry wit face"),
("Giancarlo Esposito","M",9,0,{"sy":.86,"jd":.72},"Gus Fring precise face"),
("Matt Smith","M",9,5,{"fp":.58,"sy":.83},"Doctor Who long face"),
("David Tennant","M",9,5,{"sy":.85,"es":.55},"Scottish Doctor face"),
("Jenna Coleman","F",9,0,{"sy":.87,"ck":.68},"British companion face"),
("Millie Alcock","F",9,3,{"sy":.86,"ft":.60},"Young Rhaenyra face"),
("Nikolaj Coster-Waldau","M",9,2,{"jd":.80,"sy":.87},"Jaime Lannister jaw"),
("Peter Dinklage","M",9,0,{"sy":.85,"jd":.68},"Tyrion sharp features"),
("Gwendoline Christie","F",9,5,{"jd":.68,"fp":.56},"Brienne tall face"),
("Maisie Williams","F",9,3,{"sy":.85,"ft":.62},"Arya Stark sharp face"),
("Julia Garner","F",9,0,{"sy":.86,"ck":.70},"Ruth Langmore curls"),
("Anya Chalotra","F",9,0,{"sy":.87,"ck":.70},"Yennefer dark beauty"),
("Oprah Winfrey","F",9,1,{"sy":.86,"lf":.58},"Media queen warm face"),
("Ellen DeGeneres","F",9,0,{"sy":.85,"jd":.58},"Talk show host face"),
("Trevor Noah","M",9,0,{"sy":.87,"jd":.68},"SA comedian sharp face"),
("Stephen Colbert","M",9,0,{"sy":.85,"jd":.65},"Late night host ears"),
("Jimmy Fallon","M",9,1,{"sy":.85,"fr":.59},"Tonight Show smile"),
("James Corden","M",9,1,{"sy":.83,"fr":.61},"British round-faced host"),
("Ryan Seacrest","M",9,0,{"sy":.86,"jd":.68},"TV host clean face"),
("Jimmy Kimmel","M",9,1,{"sy":.84,"fr":.59},"Late night host face"),
("Conan O'Brien","M",9,5,{"fp":.62,"fr":.46},"Red-haired tall face"),
("Seth Meyers","M",9,0,{"sy":.85,"jd":.65},"Late Night SNL face"),
("John Oliver","M",9,0,{"sy":.84,"fp":.56},"British satirist face"),
("Sarah Jessica Parker","F",9,5,{"ck":.72,"sy":.85},"Carrie elongated face"),
("Ian Somerhalder","M",9,0,{"sy":.88,"ct":.58},"Vampire blue eyes"),
("Nina Dobrev","F",9,0,{"sy":.88,"ck":.70},"Bulgarian doppelganger"),
("Paul Wesley","M",9,0,{"sy":.87,"jd":.72},"Stefan vampire face"),
("Jensen Ackles","M",9,2,{"jd":.80,"sy":.88},"Dean Winchester jaw"),
("Jared Padalecki","M",9,5,{"sy":.86,"jd":.72},"Sam tall-faced hunter"),
("Norman Reedus","M",9,5,{"sy":.83,"jd":.72},"Daryl rugged face"),
("Lauren Cohan","F",9,0,{"sy":.87,"ck":.68},"Maggie green-eyed face"),
("Jon Bernthal","M",9,2,{"jd":.80,"sy":.85},"Punisher broken nose"),
("Kunal Nayyar","M",9,0,{"sy":.85,"fr":.55},"Raj Koothrappali face"),
("Danny DeVito","M",9,1,{"sy":.82,"fr":.62},"Compact round icon"),
("Jeff Bridges","M",9,0,{"sy":.84,"jd":.68},"The Dude rugged face"),
("Mark Hamill","M",9,0,{"sy":.84,"jd":.65},"Luke Skywalker face"),
("Charlie Cox","M",9,0,{"sy":.86,"jd":.68},"Daredevil handsome face"),
("Tatiana Maslany","F",9,0,{"sy":.87,"ck":.68},"Clone-shifting face"),
("Ke Huy Quan","M",9,0,{"sy":.86,"jd":.65},"Multiverse comeback face"),
("Diego Luna","M",9,0,{"sy":.86,"lf":.55},"Cassian Andor face"),
("Tenoch Huerta","M",9,0,{"sy":.85,"jd":.68},"Namor striking face"),
("Wagner Moura","M",9,0,{"sy":.85,"jd":.68},"Narcos Pablo face"),
("Alvaro Morte","M",9,0,{"sy":.86,"jd":.72},"Professor heist face"),
("Benedict Wong","M",9,1,{"sy":.85,"fr":.60},"Wong warm round face"),
("Henry Winkler","M",9,1,{"sy":.84,"fr":.59},"Fonzie classic face"),
# ═══ Models (50) ═══
("Bella Hadid","F",10,4,{"ck":.82,"sy":.91},"Golden ratio supermodel"),
("Kendall Jenner","F",10,0,{"sy":.89,"ck":.72},"Runway angular beauty"),
("Adriana Lima","F",10,3,{"sy":.90,"ck":.75},"VS angel cat eyes"),
("Tyson Beckford","M",10,2,{"jd":.82,"sy":.90},"Male model icon jaw"),
("Gigi Hadid","F",10,0,{"sy":.89,"ck":.70},"California supermodel"),
("Naomi Campbell","F",10,4,{"ck":.78,"sy":.90},"OG supermodel cheekbones"),
("Cindy Crawford","F",10,0,{"sy":.89,"gr":.86},"Iconic mole beauty"),
("Kate Moss","F",10,3,{"sy":.87,"ft":.62},"Waif model icon"),
("Heidi Klum","F",10,0,{"sy":.88,"gr":.85},"Project Runway beauty"),
("Gisele Bundchen","F",10,0,{"sy":.89,"gr":.87},"Brazilian supermodel"),
("Cara Delevingne","F",10,3,{"sy":.87,"ck":.72},"Bold brow icon"),
("Miranda Kerr","F",10,3,{"sy":.89,"gr":.86},"VS angel dimples"),
("Karlie Kloss","F",10,5,{"sy":.88,"ck":.72},"Tall angular model"),
("Joan Smalls","F",10,0,{"sy":.88,"ck":.72},"Puerto Rican beauty"),
("Iman","F",10,0,{"sy":.90,"ck":.78},"Somali supermodel queen"),
("Tyra Banks","F",10,0,{"sy":.88,"ck":.72},"Smize queen face"),
("Claudia Schiffer","F",10,0,{"sy":.89,"gr":.86},"German blonde icon"),
("Christy Turlington","F",10,0,{"sy":.89,"gr":.87},"Timeless model face"),
("Linda Evangelista","F",10,0,{"sy":.89,"ck":.72},"Chameleon supermodel"),
("Behati Prinsloo","F",10,0,{"sy":.88,"ck":.70},"Namibian VS angel"),
("Alessandra Ambrosio","F",10,0,{"sy":.89,"gr":.86},"Brazilian model queen"),
("Candice Swanepoel","F",10,0,{"sy":.89,"gr":.86},"SA blonde angel"),
("Doutzen Kroes","F",10,0,{"sy":.89,"ck":.72},"Dutch supermodel face"),
("Liu Wen","F",10,0,{"sy":.88,"ck":.70},"Chinese supermodel icon"),
("Alek Wek","F",10,0,{"sy":.88,"ck":.75},"Sudanese striking beauty"),
("Ashley Graham","F",10,1,{"sy":.87,"lf":.58},"Curvy model pioneer"),
("Winnie Harlow","F",10,0,{"sy":.87,"ck":.72},"Vitiligo beauty icon"),
("Adut Akech","F",10,0,{"sy":.89,"ck":.78},"South Sudanese model"),
("Lucky Blue Smith","M",10,0,{"sy":.89,"gr":.86},"Blue-eyed blonde model"),
("Sean O'Pry","M",10,0,{"sy":.90,"gr":.88},"Most-booked male model"),
("David Gandy","M",10,2,{"jd":.85,"sy":.90},"D&G blue steel jaw"),
("Jon Kortajarena","M",10,0,{"sy":.89,"ck":.72},"Spanish model cheeks"),
("Irina Shayk","F",10,0,{"sy":.89,"ck":.75},"Russian supermodel face"),
("Rosie Huntington-Whiteley","F",10,0,{"sy":.89,"ck":.72},"VS lips and bones"),
("Hailey Bieber","F",10,0,{"sy":.89,"jd":.65},"Baldwin model jawline"),
("Emily Ratajkowski","F",10,0,{"sy":.88,"lf":.62},"Blurred Lines beauty"),
("Chrissy Teigen","F",10,1,{"sy":.87,"lf":.58},"Model mom round face"),
("Kaia Gerber","F",10,0,{"sy":.89,"ck":.72},"Crawford genes beauty"),
("Vittoria Ceretti","F",10,0,{"sy":.89,"gr":.86},"Italian next-gen model"),
("Lara Stone","F",10,2,{"sy":.87,"jd":.68},"Gap-toothed Dutch model"),
("Natalia Vodianova","F",10,0,{"sy":.89,"gr":.86},"Russian fairy-tale face"),
("Suki Waterhouse","F",10,0,{"sy":.87,"ck":.68},"British model-actress"),
("Georgia May Jagger","F",10,0,{"sy":.87,"lf":.58},"Jagger lips genetics"),
("Jordan Barrett","M",10,0,{"sy":.89,"ct":.58},"Alien blue-eyed model"),
("Francisco Lachowski","M",10,0,{"sy":.91,"gr":.89},"Brazilian male model"),
("Paloma Elsesser","F",10,1,{"sy":.87,"lf":.58},"Inclusive beauty icon"),
("Baptiste Giabiconi","M",10,0,{"sy":.89,"jd":.72},"Chanel muse model"),
("Andreja Pejic","F",10,0,{"sy":.89,"ck":.72},"Androgynous icon face"),
("Bar Refaeli","F",10,0,{"sy":.89,"gr":.86},"Israeli blonde beauty"),
("Slick Woods","F",10,4,{"ck":.75,"sy":.87},"Gap-tooth Fenty model"),
# ═══ Historical / Iconic (60) ═══
("Marilyn Monroe","F",11,3,{"lf":.68,"sy":.89},"Iconic beauty mark"),
("Audrey Hepburn","F",11,0,{"sy":.90,"gr":.88},"Elegance personified"),
("James Dean","M",11,0,{"sy":.87,"jd":.72},"Rebel cool jawline"),
("Princess Diana","F",11,3,{"sy":.88,"ck":.70},"People's princess face"),
("Elvis Presley","M",11,2,{"jd":.80,"lf":.62},"King's lips and jaw"),
("Grace Kelly","F",11,0,{"sy":.91,"gr":.90},"Monaco princess perfection"),
("Elizabeth Taylor","F",11,0,{"sy":.90,"lf":.62},"Violet-eyed beauty"),
("Sophia Loren","F",11,0,{"sy":.89,"lf":.62},"Italian screen goddess"),
("Brigitte Bardot","F",11,0,{"sy":.89,"lf":.62},"French kitten pout"),
("Cary Grant","M",11,0,{"sy":.89,"gr":.86},"Debonair cleft chin"),
("Clark Gable","M",11,2,{"jd":.80,"sy":.86},"King of Hollywood jaw"),
("Humphrey Bogart","M",11,5,{"sy":.83,"jd":.72},"Bogie tough-guy face"),
("Marlon Brando","M",11,2,{"jd":.82,"lf":.60},"Streetcar massive jaw"),
("Paul Newman","M",11,0,{"sy":.90,"gr":.88},"Blue-eyed perfection"),
("Steve McQueen","M",11,2,{"jd":.80,"sy":.86},"King of cool jaw"),
("Sean Connery","M",11,2,{"jd":.80,"sy":.86},"007 Scottish jaw"),
("Raquel Welch","F",11,0,{"sy":.89,"ck":.72},"Bombshell features"),
("Jane Fonda","F",11,0,{"sy":.87,"ck":.70},"Activist beauty"),
("Catherine Deneuve","F",11,0,{"sy":.89,"gr":.86},"French ice beauty"),
("Alain Delon","M",11,0,{"sy":.91,"gr":.89},"Most handsome Frenchman"),
("Omar Sharif","M",11,0,{"sy":.88,"ck":.68},"Doctor Zhivago dark eyes"),
("Gregory Peck","M",11,0,{"sy":.88,"jd":.75},"Atticus noble features"),
("Ingrid Bergman","F",11,0,{"sy":.89,"gr":.87},"Casablanca radiant face"),
("Lauren Bacall","F",11,0,{"sy":.88,"ck":.72},"Smoky sultry gaze"),
("Rita Hayworth","F",11,0,{"sy":.88,"lf":.58},"Gilda red-haired icon"),
("Ava Gardner","F",11,0,{"sy":.89,"lf":.60},"Most beautiful in world"),
("Vivien Leigh","F",11,0,{"sy":.89,"gr":.87},"Scarlett perfect face"),
("Gene Kelly","M",11,0,{"sy":.87,"jd":.68},"Singing in rain smile"),
("Frank Sinatra","M",11,0,{"sy":.86,"ct":.57},"Old Blue Eyes face"),
("Sidney Poitier","M",11,0,{"sy":.88,"jd":.72},"Dignified strong face"),
("Harry Belafonte","M",11,0,{"sy":.88,"gr":.84},"King of calypso face"),
("Dorothy Dandridge","F",11,0,{"sy":.88,"ck":.72},"Trailblazer beauty"),
("Josephine Baker","F",11,0,{"sy":.87,"ck":.70},"Entertainer icon face"),
("Charlie Chaplin","M",11,1,{"sy":.84,"fr":.58},"Tramp iconic mustache"),
("Greta Garbo","F",11,0,{"sy":.89,"ck":.75},"I want to be alone face"),
("Marlene Dietrich","F",11,4,{"ck":.78,"sy":.89},"Blue Angel cheekbones"),
("Bette Davis","F",11,1,{"es":.58,"sy":.86},"What-a-dump eyes"),
("Katharine Hepburn","F",11,0,{"sy":.87,"ck":.72},"Yankee aristocrat face"),
("Lena Horne","F",11,0,{"sy":.88,"ck":.72},"Stormy Weather beauty"),
("Anna May Wong","F",11,0,{"sy":.88,"ck":.70},"First Asian star face"),
("Bruce Lee","M",11,0,{"sy":.88,"jd":.75},"Dragon intense face"),
("Jackie Chan","M",11,1,{"sy":.85,"fr":.59},"Drunken master smile"),
("JFK","M",11,0,{"sy":.87,"gr":.84},"Presidential classic face"),
("Michelle Obama","F",11,0,{"sy":.88,"jd":.65},"First Lady strong face"),
("Barack Obama","M",11,0,{"sy":.88,"gr":.84},"Presidential symmetry"),
("Jacqueline Kennedy","F",11,0,{"sy":.89,"ck":.72},"First Lady elegance"),
("Mahatma Gandhi","M",11,1,{"sy":.83,"fr":.58},"Bespectacled icon"),
("Nelson Mandela","M",11,1,{"sy":.85,"lf":.56},"Madiba warm smile"),
("Frida Kahlo","F",11,0,{"sy":.84,"es":.48},"Unibrow icon features"),
("Queen Elizabeth II","F",11,1,{"sy":.85,"fr":.58},"Royal composure face"),
("Martin Luther King Jr.","M",11,1,{"sy":.86,"lf":.58},"Dream orator face"),
("Rudolph Valentino","M",11,5,{"sy":.87,"ck":.72},"Silent film heartthrob"),
("Errol Flynn","M",11,0,{"sy":.87,"jd":.72},"Swashbuckler mustache"),
("Sammy Davis Jr.","M",11,0,{"sy":.85,"es":.55},"Rat Pack glass-eyed"),
("Judy Garland","F",11,1,{"sy":.86,"es":.55},"Wizard of Oz eyes"),
("Jet Li","M",11,0,{"sy":.87,"jd":.68},"Wushu master face"),
("Cleopatra","F",11,0,{"sy":.86,"ck":.72},"Legendary ruler beauty"),
("Nefertiti","F",11,5,{"sy":.88,"ck":.78},"Egyptian queen structure"),
("Diana Ross","F",11,0,{"sy":.87,"ck":.72},"Supreme diva features"),
("Aaliyah","F",11,0,{"sy":.88,"ck":.70},"R&B princess beauty"),
# ═══ Tech / Business (50) ═══
("Elon Musk","M",12,2,{"jd":.72,"sy":.83},"Mars-bound square face"),
("Mark Zuckerberg","M",12,1,{"sy":.84,"fr":.58},"Metaverse round face"),
("Sundar Pichai","M",12,0,{"sy":.86,"jd":.65},"Google calm oval face"),
("Jeff Bezos","M",12,1,{"sy":.84,"fp":.58},"Bald billionaire dome"),
("Tim Cook","M",12,0,{"sy":.85,"jd":.65},"Apple CEO sharp face"),
("Bill Gates","M",12,1,{"sy":.84,"fp":.56},"Microsoft nerd face"),
("Steve Jobs","M",12,5,{"sy":.85,"ck":.68},"Apple visionary face"),
("Jack Dorsey","M",12,5,{"sy":.84,"jd":.68},"Bearded tech face"),
("Jensen Huang","M",12,0,{"sy":.85,"jd":.65},"Nvidia leather jacket"),
("Satya Nadella","M",12,1,{"sy":.85,"fr":.58},"Microsoft warm face"),
("Lisa Su","F",12,0,{"sy":.86,"jd":.62},"AMD CEO composed face"),
("Sheryl Sandberg","F",12,0,{"sy":.87,"ck":.68},"Lean In strong face"),
("Marissa Mayer","F",12,0,{"sy":.86,"ck":.68},"Yahoo blonde precision"),
("Susan Wojcicki","F",12,0,{"sy":.85,"jd":.60},"YouTube exec face"),
("Indra Nooyi","F",12,0,{"sy":.86,"ck":.68},"Pepsi CEO strong face"),
("Mukesh Ambani","M",12,1,{"sy":.83,"fr":.62},"India richest face"),
("Ratan Tata","M",12,0,{"sy":.86,"jd":.68},"Indian icon dignified"),
("Jack Ma","M",12,1,{"sy":.82,"fr":.58},"Alibaba unique face"),
("Larry Page","M",12,0,{"sy":.84,"fp":.55},"Google co-founder face"),
("Sergey Brin","M",12,1,{"sy":.84,"fr":.58},"Google co-founder face"),
("Reed Hastings","M",12,0,{"sy":.84,"fp":.56},"Netflix CEO face"),
("Brian Chesky","M",12,0,{"sy":.85,"jd":.68},"Airbnb designer face"),
("Patrick Collison","M",12,5,{"sy":.84,"fr":.48},"Stripe Irish tall face"),
("Evan Spiegel","M",12,0,{"sy":.86,"jd":.68},"Snapchat CEO face"),
("Sam Altman","M",12,0,{"sy":.85,"jd":.65},"OpenAI CEO round face"),
("Demis Hassabis","M",12,0,{"sy":.85,"jd":.65},"DeepMind chess face"),
("Peter Thiel","M",12,0,{"sy":.84,"jd":.68},"PayPal mafia face"),
("Marc Andreessen","M",12,1,{"sy":.83,"fp":.60},"VC massive forehead"),
("Richard Branson","M",12,0,{"sy":.84,"lf":.55},"Virgin beard smile"),
("Warren Buffett","M",12,1,{"sy":.83,"fr":.59},"Oracle of Omaha face"),
("Kylie Jenner","F",12,0,{"lf":.68,"sy":.87},"Lip kit mogul lips"),
("Kim Kardashian","F",12,0,{"sy":.88,"ck":.72},"Contour queen face"),
("Mark Cuban","M",12,2,{"jd":.72,"sy":.84},"Shark Tank square face"),
("Gary Vaynerchuk","M",12,0,{"sy":.83,"jd":.68},"Hustle energy face"),
("Tony Robbins","M",12,2,{"jd":.78,"fr":.60},"Massive motivator face"),
("Arianna Huffington","F",12,0,{"sy":.86,"ck":.68},"Media mogul face"),
("Whitney Wolfe Herd","F",12,0,{"sy":.87,"ck":.68},"Bumble CEO face"),
("Falguni Nayar","F",12,0,{"sy":.86,"jd":.60},"Nykaa founder face"),
("Byju Raveendran","M",12,0,{"sy":.84,"jd":.65},"Edtech founder face"),
("Ritesh Agarwal","M",12,1,{"sy":.84,"fr":.57},"OYO young CEO face"),
("Nikhil Kamath","M",12,0,{"sy":.85,"jd":.68},"Zerodha sharp face"),
("Bernard Arnault","M",12,0,{"sy":.85,"jd":.68},"LVMH French mogul"),
("Reid Hoffman","M",12,1,{"sy":.83,"fr":.60},"LinkedIn round face"),
("Travis Kalanick","M",12,0,{"sy":.84,"jd":.68},"Uber founder face"),
("Drew Houston","M",12,0,{"sy":.84,"fr":.55},"Dropbox quiet face"),
("Kevin Systrom","M",12,0,{"sy":.85,"jd":.68},"Instagram founder face"),
("Jan Koum","M",12,2,{"jd":.72,"sy":.83},"WhatsApp quiet jaw"),
("Masayoshi Son","M",12,1,{"sy":.83,"fr":.59},"SoftBank vision face"),
("Ginni Rometty","F",12,0,{"sy":.86,"jd":.62},"IBM CEO strong face"),
("Payal Kadakia","F",12,0,{"sy":.86,"ck":.68},"ClassPass founder face"),
# ═══ South Indian (60) ═══
("Allu Arjun","M",13,0,{"sy":.89,"gr":.86},"Pushpa icon features"),
("Ram Charan","M",13,2,{"jd":.80,"sy":.88},"RRR warrior jawline"),
("Vijay","M",13,0,{"sy":.87,"ck":.68},"Thalapathy mass face"),
("Rajinikanth","M",13,0,{"sy":.84,"ck":.65},"Superstar iconic face"),
("Kamal Haasan","M",13,5,{"sy":.85,"ck":.68},"Ulaganayagan versatile"),
("Ajith Kumar","M",13,2,{"jd":.78,"sy":.85},"Thala salt-pepper face"),
("Vikram","M",13,0,{"sy":.86,"jd":.70},"Chiyaan chameleon face"),
("Suriya","M",13,0,{"sy":.87,"jd":.70},"Bright intense face"),
("Dhanush","M",13,4,{"ck":.72,"sy":.84},"Lean angular cheekbones"),
("Prabhas","M",13,2,{"jd":.78,"fr":.59},"Baahubali massive jaw"),
("Mahesh Babu","M",13,0,{"sy":.89,"gr":.85},"Prince Telugu cinema"),
("Jr. NTR","M",13,1,{"sy":.85,"jd":.68},"Dynamic star features"),
("Yash","M",13,2,{"jd":.80,"sy":.86},"KGF rocky rugged jaw"),
("Dulquer Salmaan","M",13,0,{"sy":.88,"gr":.84},"Pan-Indian charming face"),
("Tovino Thomas","M",13,0,{"sy":.87,"jd":.68},"Malayali refined face"),
("Prithviraj Sukumaran","M",13,2,{"jd":.78,"sy":.86},"Strong commander jaw"),
("Mohanlal","M",13,1,{"sy":.84,"lf":.55},"Lalettan expressive face"),
("Mammootty","M",13,0,{"sy":.86,"jd":.72},"Megastar dignified face"),
("Fahadh Faasil","M",13,0,{"sy":.85,"es":.53},"Intense watchful eyes"),
("Nivin Pauly","M",13,1,{"sy":.84,"fr":.59},"Friendly Malayali face"),
("Naga Chaitanya","M",13,0,{"sy":.86,"jd":.65},"Soft refined features"),
("Rana Daggubati","M",13,2,{"jd":.85,"fr":.61},"Massive imposing jaw"),
("Vijay Sethupathi","M",13,1,{"sy":.83,"lf":.56},"Makkal Selvan face"),
("Sivakarthikeyan","M",13,1,{"sy":.84,"fr":.58},"Boy-next-door Tamil"),
("Karthi","M",13,0,{"sy":.85,"jd":.70},"Paruthiveeran sharp face"),
("Vijay Deverakonda","M",13,0,{"sy":.87,"jd":.72},"Arjun Reddy intense"),
("Naveen Polishetty","M",13,1,{"sy":.85,"fr":.58},"Jathi Ratnalu comedy"),
("Vishal","M",13,2,{"jd":.78,"fr":.58},"Action hero broad jaw"),
("Arya","M",13,0,{"sy":.85,"jd":.68},"Romantic hero features"),
("Jayam Ravi","M",13,0,{"sy":.86,"lf":.55},"Boyish Tamil features"),
("Unni Mukundan","M",13,2,{"jd":.80,"sy":.86},"Athletic sculpted jaw"),
("Dileep","M",13,1,{"sy":.82,"fr":.59},"Janapriyan comedy face"),
("Ravi Teja","M",13,1,{"sy":.83,"jd":.62},"Mass Maharaja energy"),
("Nani","M",13,0,{"sy":.85,"lf":.52},"Natural star natural face"),
("Ram Pothineni","M",13,0,{"sy":.86,"jd":.68},"RAPO energetic face"),
("Nayanthara","F",13,0,{"sy":.89,"ck":.72},"Lady Superstar beauty"),
("Samantha Ruth Prabhu","F",13,0,{"sy":.88,"ck":.72},"Versatile queen face"),
("Sai Pallavi","F",13,0,{"sy":.88,"ct":.58},"Natural no-makeup face"),
("Nithya Menen","F",13,1,{"sy":.86,"lf":.56},"Warm versatile beauty"),
("Keerthy Suresh","F",13,1,{"sy":.87,"lf":.56},"Mahanati dimpled face"),
("Trisha Krishnan","F",13,0,{"sy":.88,"ck":.70},"South queen features"),
("Anushka Shetty","F",13,0,{"sy":.88,"ck":.72},"Devasena regal face"),
("Tamannaah Bhatia","F",13,0,{"sy":.88,"lf":.58},"Milky beauty face"),
("Kajal Aggarwal","F",13,0,{"sy":.87,"ck":.68},"Bright south beauty"),
("Shruti Haasan","F",13,0,{"sy":.87,"ck":.70},"Rock-star model face"),
("Aishwarya Lekshmi","F",13,0,{"sy":.87,"ck":.68},"Doctor actress beauty"),
("Pooja Hegde","F",13,0,{"sy":.88,"gr":.85},"Pan-Indian star face"),
("Rashmika Mandanna","F",13,3,{"sy":.88,"ft":.60},"National crush dimples"),
("Parvathy Thiruvothu","F",13,0,{"sy":.86,"ck":.68},"Indie Malayalam beauty"),
("Malavika Mohanan","F",13,0,{"sy":.87,"ck":.70},"Beyond Clouds beauty"),
("Nazriya Nazim","F",13,3,{"sy":.87,"ft":.60},"Cute Malayali face"),
("Manju Warrier","F",13,0,{"sy":.87,"ck":.68},"Lady superstar Kerala"),
("Jyothika","F",13,0,{"sy":.87,"ck":.68},"Tamil queen features"),
("Ramya Krishnan","F",13,0,{"sy":.86,"lf":.58},"Sivagami regal face"),
("Andrea Jeremiah","F",13,0,{"sy":.87,"ck":.70},"Multi-talented beauty"),
("Amala Paul","F",13,0,{"sy":.87,"lf":.56},"Bright-eyed south beauty"),
("Rashi Khanna","F",13,0,{"sy":.87,"ck":.68},"Tollywood bright face"),
("Sree Leela","F",13,0,{"sy":.87,"ck":.68},"Rising Telugu star face"),
("Meena","F",13,1,{"sy":.86,"lf":.56},"Evergreen south beauty"),
("Madonna Sebastian","F",13,3,{"sy":.86,"ft":.60},"Premam cute face"),
]

assert len(D) == 1000, f"Expected 1000 celebrities, got {len(D)}"

# ── Generate vectors and write output file ──
MATCHING_CODE = r'''
DIMENSION_NAMES = [
    "face_ratio", "symmetry", "eye_spacing", "canthal_tilt",
    "nose_proportion", "lip_fullness", "lip_ratio", "jaw_definition",
    "cheekbone_height", "forehead_proportion", "face_taper", "golden_ratio",
]

DIMENSION_LABELS = [
    "Face shape ratio", "Facial symmetry", "Eye spacing", "Canthal tilt",
    "Nose proportion", "Lip fullness", "Lip ratio", "Jaw definition",
    "Cheekbone height", "Forehead proportion", "Face taper", "Golden ratio closeness",
]


def _normalize(value, lo, hi):
    """Clamp *value* into [lo, hi] then scale to 0.0-1.0."""
    if hi == lo:
        return 0.5
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))


def build_user_vector(face, eyes, brows, nose, lips, jaw, skin, harmony):
    """
    Build a 12-dimensional proportion vector (all values 0.0-1.0)
    from the analysis result dicts produced by the individual analyzers.

    Parameters
    ----------
    face    : dict from face_structure.analyze_face_structure
    eyes    : dict from eye_analyzer.analyze_eyes
    brows   : dict from brow_analyzer.analyze_brows
    nose    : dict from nose_analyzer.analyze_nose
    lips    : dict from lip_analyzer.analyze_lips
    jaw     : dict from jaw_analyzer.analyze_jaw
    skin    : dict from skin_analyzer.analyze_skin
    harmony : dict from harmony_scores.analyze_harmony
    """

    # 1. face_ratio  — width / height, typical range 0.55-0.95
    wl = face.get("widthToLengthRatio", 0.72)
    face_ratio = _normalize(wl, 0.55, 0.95)

    # 2. symmetry  — average of all symmetry scores (0-100 → 0-1)
    sym_vals = [
        face.get("symmetryScore", 80),
        eyes.get("asymmetryScore", 80),
        lips.get("symmetryScore", 80),
        jaw.get("symmetryScore", 80),
    ]
    symmetry = sum(sym_vals) / len(sym_vals) / 100.0

    # 3. eye_spacing  — from categorical + raw if available
    spacing_map = {"Close-set": 0.25, "Ideal": 0.50, "Wide-set": 0.75}
    eye_spacing = spacing_map.get(eyes.get("spacing", "Ideal"), 0.50)
    # Refine with fifths if available
    if face.get("facialFifths") == "Wide-set":
        eye_spacing = max(eye_spacing, 0.70)
    elif face.get("facialFifths") == "Close-set":
        eye_spacing = min(eye_spacing, 0.30)

    # 4. canthal_tilt  — parse the tilt string e.g. "+4.2°"
    tilt_str = eyes.get("canthalTilt", "+0°")
    try:
        tilt_deg = float(tilt_str.replace("°", "").replace("+", ""))
    except (ValueError, AttributeError):
        tilt_deg = 0.0
    canthal_tilt = _normalize(tilt_deg, -8.0, 8.0)

    # 5. nose_proportion  — nose width relative to face
    nose_cat_map = {"Narrow": 0.25, "Proportionate": 0.50, "Wide": 0.75}
    nose_proportion = nose_cat_map.get(nose.get("widthRatio", "Proportionate"), 0.50)

    # 6. lip_fullness
    full_map = {"Thin": 0.20, "Medium": 0.45, "Full": 0.70, "Very full": 0.90}
    lip_fullness = full_map.get(lips.get("fullness", "Medium"), 0.45)

    # 7. lip_ratio  — upper-to-lower ratio string "1:X"
    ratio_str = lips.get("upperLowerRatio", "1:1.6")
    try:
        parts = ratio_str.split(":")
        ul = float(parts[0])
        ll = float(parts[1]) if len(parts) > 1 else 1.0
        raw_ratio = ul / ll if ll > 0 else 1.0
    except (ValueError, IndexError):
        raw_ratio = 0.625
    lip_ratio = _normalize(raw_ratio, 0.3, 1.2)

    # 8. jaw_definition
    jaw_map = {"Undefined": 0.15, "Rounded": 0.30, "Soft": 0.45,
               "Defined": 0.70, "Sharp": 0.90}
    jaw_definition = jaw_map.get(jaw.get("type", "Defined"), 0.55)

    # 9. cheekbone_height
    ck_map = {"Low": 0.25, "Medium": 0.50, "High": 0.80}
    cheekbone_height = ck_map.get(face.get("cheekboneProminence", "Medium"), 0.50)

    # 10. forehead_proportion  — from facial thirds
    thirds_map = {"Top heavy": 0.75, "Balanced": 0.50, "Bottom heavy": 0.30}
    forehead_proportion = thirds_map.get(face.get("facialThirds", "Balanced"), 0.50)

    # 11. face_taper  — jaw width vs cheekbone width
    jw = face.get("_jawWidth", 1)
    cw = face.get("_cheekboneWidth", 1)
    if cw > 0:
        taper_raw = 1.0 - (jw / cw)
        face_taper = _normalize(taper_raw, -0.1, 0.4)
    else:
        face_taper = 0.50

    # 12. golden_ratio  — from harmony scores
    gr_raw = harmony.get("goldenRatioScore", 50)
    golden_ratio = gr_raw / 100.0

    vector = [
        round(face_ratio, 2),
        round(symmetry, 2),
        round(eye_spacing, 2),
        round(canthal_tilt, 2),
        round(nose_proportion, 2),
        round(lip_fullness, 2),
        round(lip_ratio, 2),
        round(jaw_definition, 2),
        round(cheekbone_height, 2),
        round(forehead_proportion, 2),
        round(face_taper, 2),
        round(golden_ratio, 2),
    ]
    return vector


def _cosine_similarity(a, b):
    """Cosine similarity between two equal-length vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sum(x * x for x in a) ** 0.5
    mag_b = sum(x * x for x in b) ** 0.5
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def _describe_similarities(user_vec, celeb_vec):
    """Return 2-3 human-readable similarity descriptions."""
    diffs = []
    for i, (u, c) in enumerate(zip(user_vec, celeb_vec)):
        diffs.append((abs(u - c), i))
    diffs.sort()

    descriptions = []
    threshold = 0.08
    labels = {
        0: "Similar face shape",
        1: "Matching facial symmetry",
        2: "Close eye spacing",
        3: "Similar canthal tilt",
        4: "Matching nose proportion",
        5: "Similar lip fullness",
        6: "Close lip ratio",
        7: "Matching jaw definition",
        8: "Similar cheekbone structure",
        9: "Matching forehead proportion",
        10: "Similar face taper",
        11: "Close golden ratio score",
    }
    for diff_val, idx in diffs:
        if len(descriptions) >= 3:
            break
        if diff_val <= threshold or len(descriptions) < 2:
            descriptions.append(labels[idx])
    return descriptions


def find_celebrity_matches(user_vector, top_n=5, gender_filter=None):
    """
    Find the top-N celebrity matches for a user vector.

    Parameters
    ----------
    user_vector   : list[float]  – 12-dim vector from build_user_vector()
    top_n         : int          – number of matches to return (default 5)
    gender_filter : str or None  – "M", "F", or None for all

    Returns
    -------
    list[dict] with keys:
        name, matchPercent, category, faceShape, funFact, similarities
    """
    results = []
    for celeb in CELEBRITIES:
        if gender_filter and celeb["gender"] != gender_filter:
            continue
        sim = _cosine_similarity(user_vector, celeb["vector"])
        results.append((sim, celeb))

    results.sort(key=lambda x: x[0], reverse=True)
    top = results[:top_n]

    matches = []
    for sim, celeb in top:
        pct = round(sim * 100, 1)
        pct = min(99.9, max(0.1, pct))
        matches.append({
            "name":         celeb["name"],
            "matchPercent":  pct,
            "category":     celeb["category"],
            "faceShape":    celeb["face_shape"],
            "funFact":      celeb["fun_fact"],
            "similarities": _describe_similarities(user_vector, celeb["vector"]),
        })
    return matches
'''


def generate():
    entries = []
    for name, g, ci, si, ov, fact in D:
        vec = make_vec(name, g, si, ov)
        entries.append({
            "name": name, "gender": g, "category": CATS[ci],
            "face_shape": SHAPES[si], "vector": vec, "fun_fact": fact,
        })

    out_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "celebrity_matcher.py")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write('"""\nCelebrity Lookalike Matching System\n')
        f.write(f"Auto-generated database of {len(entries)} celebrities with\n")
        f.write("pre-computed 12-dimensional facial proportion vectors.\n")
        f.write('"""\n\n')

        f.write("CELEBRITIES = [\n")
        for e in entries:
            line = "    {"
            line += f'"name": {json.dumps(e["name"])}, '
            line += f'"gender": {json.dumps(e["gender"])}, '
            line += f'"category": {json.dumps(e["category"])}, '
            line += f'"face_shape": {json.dumps(e["face_shape"])}, '
            line += f'"vector": {e["vector"]}, '
            line += f'"fun_fact": {json.dumps(e["fun_fact"])}'
            line += "},\n"
            f.write(line)
        f.write("]\n")

        f.write(MATCHING_CODE)

    print(f"✅ Generated {out_path} with {len(entries)} celebrities")
    # Quick sanity checks
    vecs = [e["vector"] for e in entries]
    unique_vecs = set(tuple(v) for v in vecs)
    print(f"   Unique vectors: {len(unique_vecs)} / {len(entries)}")
    for v in vecs:
        assert len(v) == 12
        assert all(0.0 <= x <= 1.0 for x in v), f"Out of range: {v}"


if __name__ == "__main__":
    generate()
