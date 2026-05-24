"""
Enrich all 33 composers with full biographies, updated short bios, image URLs,
and additional famous compositions.

Run with:
    DATABASE_URL="postgresql://..." python3 seeds/seed_composer_biographies.py
"""

import os
import subprocess
import sys
import tempfile

# ---------------------------------------------------------------------------
# Biography data
# ---------------------------------------------------------------------------

BIOGRAPHIES = {
    "Johann Sebastian Bach": {
        "biography_short": "German Baroque composer and organist, widely regarded as one of the greatest composers in Western musical history. Master of counterpoint, harmony, and musical structure.",
        "biography": """Johann Sebastian Bach (1685–1750) was a German composer and musician of the late Baroque period whose work has influenced virtually every subsequent Western composer. Born in Eisenach, Thuringia, into a family of musicians, he worked successively as organist in Arnstadt and Mühlhausen, court musician in Weimar, and Kapellmeister in Cöthen, before settling as Thomaskantor in Leipzig — a position he held for the final 27 years of his life.

Bach's output spans nearly every musical genre of his era except opera: over 1,000 surviving works including sacred cantatas, orchestral suites, keyboard preludes and fugues, masses, passions, and concertos. His two great collections of preludes and fugues, The Well-Tempered Clavier, traverse all 24 major and minor keys and remain cornerstone studies in keyboard technique and tonal harmony. The Brandenburg Concertos (1721) are the jewels of Baroque orchestral writing, and the Mass in B Minor stands as one of the supreme choral works ever written.

Bach was largely forgotten after his death, until Felix Mendelssohn's famous revival of the St Matthew Passion in 1829 sparked a renaissance of interest. Today he is revered not just as a historical figure but as a living presence in concert halls worldwide — his music studied, performed, and loved by musicians of every tradition.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Johann_Sebastian_Bach.jpg/440px-Johann_Sebastian_Bach.jpg",
    },
    "Wolfgang Amadeus Mozart": {
        "biography_short": "Austrian prodigy and master of the Classical period, composing over 800 works spanning every genre — opera, symphony, chamber music, and sacred music.",
        "biography": """Wolfgang Amadeus Mozart (1756–1791) was an Austrian composer and pianist whose music represents the apex of the Classical style. Born in Salzburg to a court musician father, he displayed extraordinary talent from earliest childhood, performing for European royalty at age six and composing his first symphonies before he was ten. His abbreviated life — he died at 35 — produced over 800 catalogued works.

Mozart mastered every form he touched. His 41 symphonies trace a remarkable evolution from polished entertainment to profound expression; the final trilogy — Nos. 39, 40, and 41 (Jupiter) — composed in six weeks in 1788, remain summit works of the orchestral repertoire. His piano concertos (27 in all) invented a new balance between soloist and orchestra. In opera he was peerless: Le Nozze di Figaro (1786), Don Giovanni (1787), and Die Zauberflöte (1791) are among the most performed operas in history, combining dramatic truth, memorable melody, and harmonic ingenuity.

His unfinished Requiem, left incomplete at his death, has become one of the most mythologised works in music history. Mozart's gift — the seemingly effortless marriage of beauty and depth — has made him the archetypal image of musical genius across cultures and centuries.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Croce-Mozart-Detail.jpg/440px-Croce-Mozart-Detail.jpg",
    },
    "Ludwig van Beethoven": {
        "biography_short": "German composer who bridged the Classical and Romantic eras; composed nine symphonies, five piano concertos, and 32 piano sonatas, including much of his greatest work while profoundly deaf.",
        "biography": """Ludwig van Beethoven (1770–1827) was a German composer and pianist who remains one of the most influential figures in the history of Western music. Born in Bonn, he moved to Vienna in 1792 to study with Haydn, and spent the rest of his life there transforming the musical language he inherited from Mozart and Haydn into something altogether more dramatic, personal, and far-reaching.

Beethoven's progressive hearing loss — which became severe by his mid-thirties and total by his late forties — is among the most poignant stories in musical biography. Yet it was in this period of encroaching silence that he wrote some of his greatest works: the Fifth and Seventh Symphonies, the late string quartets, the Missa Solemnis, and the Ninth Symphony, premiered in 1824 when he was completely deaf. The Ninth — with its final choral movement setting Schiller's "Ode to Joy" — was the first symphony to incorporate the human voice, and its opening theme has become perhaps the most recognised melody in the Western canon.

His 32 piano sonatas chart the evolution of the instrument and its possibilities; works like the "Moonlight" Sonata (Op. 27 No. 2) and the "Hammerklavier" (Op. 106) remain touchstones for pianists today. Beethoven expanded every form he touched — the symphony, the string quartet, the piano concerto — establishing a model of the composer as heroic individual, expressing subjective experience through music, that shaped the entire Romantic era.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Beethoven.jpg/440px-Beethoven.jpg",
    },
    "Antonio Vivaldi": {
        "biography_short": "Italian Baroque composer, virtuoso violinist and ordained priest, best known for The Four Seasons — a set of violin concertos that became the most recorded classical work of all time.",
        "biography": """Antonio Vivaldi (1678–1741) was an Italian composer, virtuoso violinist, and Roman Catholic priest, born in Venice. He spent much of his career at the Ospedale della Pietà, a Venetian institution for orphaned and illegitimate girls, where he trained a world-famous orchestra and composed an enormous body of music for their performances.

Vivaldi was extraordinarily prolific: over 500 concertos, more than 40 operas, sacred choral works, and chamber music. His concertos for violin, oboe, lute, and other instruments established the three-movement concerto form that would dominate instrumental music for the rest of the Baroque period and beyond. His most famous work, the set of four violin concertos known as The Four Seasons (1725), is arguably the most recorded piece of classical music in history. Each concerto depicts a season through vivid tone-painting — the chirping of birds in Spring, the oppressive heat of Summer, a harvest dance in Autumn, and the biting cold of Winter — accompanied by sonnets that may have been written by Vivaldi himself.

Vivaldi died in Vienna in poverty and was buried in a pauper's grave, his reputation having dimmed considerably in his final years. The twentieth century saw a spectacular rediscovery of his music: Bach transcribed several of his concertos, and today his works are performed and recorded worldwide.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Vivaldi.jpg/440px-Vivaldi.jpg",
    },
    "George Frideric Handel": {
        "biography_short": "German-born British Baroque composer renowned for Messiah, Water Music, and Music for the Royal Fireworks; one of the most celebrated composers of the Baroque era.",
        "biography": """George Frideric Handel (1685–1759) was a German-born composer who spent most of his career in England and became a naturalized British subject. Born in Halle the same year as Bach, he studied in Hamburg and Italy before settling permanently in London in 1712, where he became the dominant figure in English musical life for over four decades.

Handel began his English career as an opera composer, writing nearly 40 Italian-style operas for the London stage. When fashions changed and Italian opera fell out of favour, he reinvented himself as a composer of English oratorios — large-scale dramatic works for soloists, chorus, and orchestra, performed in concert rather than staged. His Messiah (1741), composed in just 24 days, is the most performed choral work in the Western tradition. Its "Hallelujah" chorus, according to enduring legend, prompted King George II to stand — beginning a tradition observed in concert halls worldwide to this day.

His orchestral works — the Water Music suites (1717), written for a royal river pageant on the Thames, and the Music for the Royal Fireworks (1749) — remain among the most joyful and inventive orchestral pieces of the Baroque era. Handel died wealthy and honoured, and was buried in Westminster Abbey, where a monument still stands to his memory.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/George_Frideric_Handel_by_Balthasar_Denner.jpg/440px-George_Frideric_Handel_by_Balthasar_Denner.jpg",
    },
    "Johannes Brahms": {
        "biography_short": "German Romantic composer who championed classical forms against the 'New German School'; his four symphonies, piano concertos, and German Requiem are central pillars of the Romantic repertoire.",
        "biography": """Johannes Brahms (1833–1897) was a German composer and pianist of the Romantic era, born in Hamburg. He spent most of his mature career in Vienna, where he became a central figure in the city's musical life. Along with Bach and Beethoven, Brahms is often grouped as one of the 'Three Bs' — the supreme masters of the German classical tradition.

Brahms was a perfectionist who destroyed as much as he published. He famously burned over 20 string quartets before he was satisfied with the two he eventually released. His four symphonies, composed between 1855 and 1885, are considered successors to Beethoven's tradition — architecturally rigorous, emotionally complex, and orchestrated with remarkable depth. The First Symphony alone took him 21 years to complete, leading conductor Hans von Bülow to call it "Beethoven's Tenth." His two piano concertos are among the most demanding in the repertoire, and his German Requiem (Ein deutsches Requiem, 1868) — setting texts chosen by Brahms himself from the Lutheran Bible — is a profoundly humane and comforting work that stands among the greatest choral compositions.

Outside the large forms, Brahms excelled in chamber music, lieder, and the piano miniature. His 21 Hungarian Dances for piano duet brought the folk idiom of Hungarian Roma music to concert audiences worldwide, and his late Intermezzi for solo piano are among the most intimate and inward pieces in the keyboard literature.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Brahms_Kohut.jpg/440px-Brahms_Kohut.jpg",
    },
    "Frédéric Chopin": {
        "biography_short": "Polish-French Romantic composer and virtuoso pianist who wrote almost exclusively for solo piano; his nocturnes, études, and ballades redefined expressive possibilities of the keyboard.",
        "biography": """Frédéric Chopin (1810–1849) was a Polish composer and virtuoso pianist of the Romantic era who spent most of his adult life in Paris. Born near Warsaw and displaying extraordinary musical gifts from childhood, he left Poland in 1830 — the year of the failed November Uprising against Russian rule — and never returned. Paris became his home, and he became the toast of its aristocratic salons.

Chopin wrote almost exclusively for the solo piano, yet within that single medium he achieved an astonishing variety: nocturnes of profound lyrical beauty; études of ferocious technical difficulty that are also perfect musical forms; ballades of dramatic narrative power; mazurkas and polonaises that evoked the folk rhythms and national spirit of his Polish homeland; and preludes — 24 short pieces that range from a few bars to several minutes and capture a vast emotional spectrum.

His style is immediately recognisable: a singing, flexible right-hand melody floating above richly chromatic harmonies in the left hand, played with a freedom of tempo (rubato) that anticipates the Impressionism of Debussy. He was deeply influenced by the Polish folk tradition and by the vocal ornaments of Italian bel canto opera. His health declined from his late twenties — he almost certainly suffered from tuberculosis — and he died in Paris at 39. Today Chopin remains among the most recorded and beloved composers in the repertoire, and the International Chopin Piano Competition, held every five years in Warsaw, is one of the most prestigious musical events in the world.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Frederic_Chopin_photo.jpeg/440px-Frederic_Chopin_photo.jpeg",
    },
    "Pyotr Ilyich Tchaikovsky": {
        "biography_short": "Russian Romantic composer whose ballets — Swan Lake, The Nutcracker, Sleeping Beauty — and symphonies are among the most beloved works in the Western canon.",
        "biography": """Pyotr Ilyich Tchaikovsky (1840–1893) was a Russian composer of the Romantic period whose melodic gift, dramatic instinct, and orchestral brilliance made him the most internationally celebrated Russian composer of the nineteenth century. Born in Votkinsk in the Ural region, he trained as a civil servant before entering the newly founded St Petersburg Conservatory and devoting himself to music.

Tchaikovsky's output spans every genre — six symphonies, three piano concertos, a violin concerto, ten operas, and dozens of orchestral pieces — but he is perhaps most identified with his three great ballets: Swan Lake (1876), Sleeping Beauty (1889), and The Nutcracker (1892). These works transformed the status of ballet music from functional accompaniment to full artistic expression, and they remain the most performed ballets in the world. His Piano Concerto No. 1, whose thunderous opening chords were once dismissed by his teacher as "unplayable," is now one of the most popular works in the concerto repertoire.

His last three symphonies — Nos. 4, 5, and 6 (Pathétique) — are deeply personal statements; the Pathétique, completed just nine days before his death, ends in a slow, dying-away finale that many hear as a farewell. Tchaikovsky's music combines Russian national colouring with Viennese Classical forms and French orchestral brilliance, creating a sound world that is instantly recognisable and endlessly moving.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Tchaikovsky_by_Reutlinger%2C_1888.jpg/440px-Tchaikovsky_by_Reutlinger%2C_1888.jpg",
    },
    "Niccolò Paganini": {
        "biography_short": "Italian Romantic-era virtuoso violinist and composer whose superhuman technique — rumoured to be diabolical — transformed violin playing permanently; his 24 Caprices remain the ultimate test of violin mastery.",
        "biography": """Niccolò Paganini (1782–1840) was an Italian violinist, guitarist, and composer, the most celebrated violin virtuoso of the nineteenth century and one of the pillars of Romanticism. Born in Genoa, he displayed prodigious talent from childhood and gave his first public concert at eleven. His adult concert tours across Europe created scenes of mass adulation unprecedented in the history of classical music — audiences wept, fainted, and genuinely believed, in many cases, that his technique was supernatural in origin.

Paganini's innovations transformed violin playing permanently. He pioneered the use of left-hand pizzicato (plucking with the same hand that presses the strings), double stops, harmonics, and extreme positions on the fingerboard that had previously been thought impossible. His 24 Caprices for solo violin, published in 1820, remain the supreme test of violin technique; the 24th Caprice has been reworked by Liszt, Brahms, Rachmaninoff, Lutosławski, and Andrew Lloyd Webber, among others.

Beyond the Caprices, his six violin concertos and various show pieces established the template for virtuoso concerto writing. His physical appearance — gaunt, pale, and mysteriously agile — fuelled rumours that he had sold his soul to the devil, a legend he reportedly enjoyed and cultivated. Paganini was also a fine guitarist and left a body of guitar music largely unknown outside specialist circles. He died in Nice in 1840; the Catholic Church initially refused him burial due to the devil rumours, and his body lay unburied for years before finally being interred in Parma.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Paganini_Scheffer_1832.jpg/440px-Paganini_Scheffer_1832.jpg",
    },
    "Claude Debussy": {
        "biography_short": "French Impressionist composer who dissolved the boundaries of traditional tonality; Clair de Lune, La Mer, and Prélude à l'après-midi d'un faune opened a new sound world that influenced all of 20th-century music.",
        "biography": """Claude Debussy (1862–1918) was a French composer whose work fundamentally altered the language of Western music. Born in Saint-Germain-en-Laye, he entered the Paris Conservatoire at age ten, where he proved a brilliant but unruly student who challenged his professors with unconventional harmonies. His encounter with Japanese gamelan music at the 1889 Paris Exposition Universelle had a lasting influence on his musical thinking.

Debussy is often labelled an "Impressionist" — a term he rejected, preferring to align himself with the Symbolist poets and the Japanese printmakers who were transforming French culture in his era. His music does not describe scenes so much as evoke sensations, moods, and the play of light and atmosphere. The Prélude à l'après-midi d'un faune (1894), a shimmering orchestral piece based on a poem by Mallarmé, marks the beginning of musical modernism; Pierre Boulez called it "the beginning of modern music." La Mer (1905), a three-movement orchestral work depicting the sea, demonstrates his mastery of orchestral colour and fluid, non-repeating form.

His piano music — above all the Préludes (two books, 1909–1913) and Images — established a new approach to the instrument, using whole-tone scales, unresolved dissonances, and the sustaining pedal to create cascading washes of sound. Clair de Lune, from the Suite bergamasque, has become one of the most beloved piano pieces ever written. Debussy died of cancer in Paris in March 1918, during the final German bombardment of the city — one of the most poignant endings in musical biography.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Claude_Debussy_circa_1908%2C_foto_av_Félix_Nadar.jpg/440px-Claude_Debussy_circa_1908%2C_foto_av_Félix_Nadar.jpg",
    },
    "Duke Ellington": {
        "biography_short": "American jazz composer, pianist, and bandleader who led his orchestra for nearly fifty years; his prolific output and orchestral innovations made him the greatest composer in the history of jazz.",
        "biography": """Duke Ellington (1899–1974) was an American composer, pianist, and bandleader who led his orchestra for nearly fifty years and became the most important composer in the history of jazz. Born Edward Kennedy Ellington in Washington D.C. into a middle-class African American family, he was playing professionally in his teens and formed his own bands in the early 1920s. His residency at the Cotton Club in Harlem (1927–1931), broadcast nationally on radio, made him a household name across America.

Ellington's genius lay in his ability to write specifically for the individual musicians in his band — their unique timbres, technical strengths, and improvisational personalities became the palette he composed for. His long partnership with arranger Billy Strayhorn, who composed Take the A Train (the band's signature tune) and dozens of other works, was one of the great creative collaborations in American music. Together they blurred the boundaries between composition and arrangement, between classical and jazz, between American and global influences.

His output was astonishing: beyond the famous standards — Mood Indigo, Sophisticated Lady, Satin Doll, It Don't Mean a Thing (If It Ain't Got That Swing) — he composed extended works that pushed jazz toward the concert hall: Black, Brown and Beige (1943), premiered at Carnegie Hall, was a musical portrait of African American history. His three Sacred Concerts (1965–1973) set jazz rhythms to religious texts in a Carnegie Hall setting. Ellington was awarded the Presidential Medal of Freedom in 1969 and remains one of the defining American artists of the twentieth century.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Duke_Ellington_-_publicity.jpg/440px-Duke_Ellington_-_publicity.jpg",
    },
    "Miles Davis": {
        "biography_short": "American jazz trumpeter, bandleader, and composer who led the evolution of jazz through multiple eras — bebop, cool jazz, modal jazz, and fusion — reinventing his sound every decade.",
        "biography": """Miles Davis (1926–1991) was an American jazz trumpeter, bandleader, and composer who stands as the single most influential figure in the post-war development of jazz. Born in Alton, Illinois, into an upper-middle-class African American family, he arrived in New York at 18 ostensibly to study at Juilliard, but instead immersed himself in the bebop revolution happening in the clubs of 52nd Street, playing alongside Charlie Parker and Dizzy Gillespie.

Davis did not merely participate in the history of jazz — he instigated it. His nonet recordings of 1949–50, collected as Birth of the Cool, launched the "cool jazz" movement. Kind of Blue (1959) — recorded in just two sessions, almost entirely in single takes — is the best-selling jazz album of all time and the definitive example of modal jazz, abandoning the rapid chord changes of bebop for spacious improvisation over scales. Bitches Brew (1970) fused jazz with electric rock and funk, creating jazz-rock fusion and influencing everything from Herbie Hancock to Radiohead.

Each of Davis's key bands introduced musicians who went on to define jazz's next era: John Coltrane, Bill Evans, Wayne Shorter, Herbie Hancock, Chick Corea, John McLaughlin. His tone — muted, lyrical, full of space and silence — was as distinctive as a human voice. In seven decades of musical evolution, Davis remained always restless, always seeking the next sound, making him the supreme model of creative reinvention.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Miles_Davis_-_1984.jpg/440px-Miles_Davis_-_1984.jpg",
    },
    "Astor Piazzolla": {
        "biography_short": "Argentine composer and bandoneón virtuoso who revolutionised tango by merging it with jazz and classical music, creating 'nuevo tango' — condemned by traditionalists but now recognised as a profound art form.",
        "biography": """Astor Piazzolla (1921–1992) was an Argentine composer and bandoneón player who transformed the traditional tango into a serious art form by fusing it with jazz harmony and classical counterpoint. Born in Mar del Plata, he spent his childhood in New York, where his father had him study the bandoneón — a German-origin concertina central to tango — and where he encountered jazz firsthand. Back in Buenos Aires, he played in traditional tango orchestras before travelling to Paris in 1954 to study composition with Nadia Boulanger.

It was Boulanger who, famously, heard Piazzolla play one of his own tango pieces and told him that this was where his true voice lay — not in the classical pastiche he had been writing. Returning to Argentina, he formed the Octeto Buenos Aires and began creating what he called "nuevo tango" — tango for listening rather than dancing, with dissonant harmonies, contrapuntal textures, and the energy of jazz improvisation woven through the dance's fundamental rhythms and melancholy.

The response from tango purists was hostile; death threats were not uncommon, and radio stations refused to play his music. But audiences outside Argentina embraced him. His international breakthrough came in the 1970s and 80s, and by the time of his death his status as the greatest Argentine composer and one of the most important figures in twentieth-century music was secure. Libertango (1974) has become one of the most covered instrumental pieces in the world; Adiós Nonino, written in grief at his father's death, is considered his masterpiece.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Astor_Piazzolla.jpg/440px-Astor_Piazzolla.jpg",
    },
    "Fela Kuti": {
        "biography_short": "Nigerian musician, composer, and political activist who created Afrobeat — a fusion of Yoruba music, jazz, and funk — and used it as a weapon of protest against military dictatorship.",
        "biography": """Fela Anikulapo Kuti (1938–1997) was a Nigerian musician, multi-instrumentalist, composer, and political activist who created Afrobeat and became one of Africa's most important cultural figures. Born in Abeokuta, southwestern Nigeria, into a prominent Yoruba family — his mother Funmilayo Ransome-Kuti was a pioneering feminist and anti-colonial activist — he studied music in London in the 1950s before travelling to the United States, where his encounter with Black Power politics and the music of James Brown radicalized both his politics and his music.

Returning to Lagos, he fused traditional Yoruba music and highlife with jazz improvisation and James Brown's funk — creating a new genre he named Afrobeat. The music was built on extended vamps: a single track might run 20 minutes, the horns and percussion building an irresistible groove while Fela sang, played saxophone, keyboards, and trumpet, and his dancers performed. His Kalakuta Republic compound in Lagos became a commune, a recording studio, and a symbol of resistance against the Nigerian military government.

The music and the politics were inseparable. Songs like Zombie (1977), a devastating satire of military obedience, and Water No Get Enemy were direct attacks on the regime. In retaliation, the army raided Kalakuta Republic in 1977, injuring over 200 people and throwing Fela's elderly mother from a window (she died months later). Fela was jailed multiple times. He continued performing and recording almost until his death from AIDS-related complications in 1997. His son Femi and grandson Made Kuti carry the tradition forward, and Afrobeat remains one of the most influential musical genres in the world.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Fela_Kuti.jpg/440px-Fela_Kuti.jpg",
    },
    "Oum Kalthoum": {
        "biography_short": "Egyptian singer, actress, and composer regarded as the greatest Arab singer of the 20th century; her recordings of classical Arabic poetry set to music are still heard across the Arab world every night.",
        "biography": """Oum Kalthoum (c. 1898–1975) — also spelled Umm Kulthum — was an Egyptian singer, actress, and composer who became the most celebrated Arab artist of the twentieth century and one of the greatest vocal artists in the history of world music. Born in a small village in the Nile Delta to a religious cantor father who taught her Quranic recitation and classical Arabic song, she began performing as a child and reached Cairo in the early 1920s.

Her voice was extraordinary — a deep, rich contralto of enormous power and range, capable of microtonal ornamentation that was itself a form of improvisation. Her monthly concerts, broadcast live on Cairo Radio from 1934 onwards, brought the Arab world to a standstill: shops closed, streets emptied, and millions of people across Egypt, Lebanon, Syria, Iraq, and beyond gathered around their radios to listen. A single song might last an hour or more, with Oum Kalthoum repeating phrases, varying her interpretation, and responding to the audience's rapturous responses in a living exchange.

Her recordings of the great twentieth-century Arabic poets — set to music by composers including Riyadh Al Sunbati, Mohammed Abdel Wahab, and Baligh Hamdi — remain the definitive interpretations: Inta Omri (You Are My Life), Al-Atlal (The Ruins), and Fakkaruni (They Reminded Me) are considered the pinnacles of the Arabic song tradition. When she died in February 1975, an estimated four million people attended her funeral in Cairo — one of the largest gatherings in Egyptian history. She remains an active presence in Arab cultural life; her recordings are played in homes, taxis, and cafés across the Arab world every day.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Umm_Kulthum_1946.jpg/440px-Umm_Kulthum_1946.jpg",
    },
    "Paco de Lucía": {
        "biography_short": "Spanish flamenco guitarist who single-handedly transformed the tradition by integrating jazz, bossa nova, and classical elements, elevating flamenco guitar from accompaniment to concert-hall art.",
        "biography": """Paco de Lucía (1947–2014) was a Spanish guitarist and composer who is universally recognised as the greatest flamenco guitarist of the twentieth century and one of the supreme virtuosos in the history of the instrument. Born Francisco Sánchez Gómez in Algeciras, Andalusia, he began studying guitar at age five under his father's strict instruction, practising up to twelve hours a day as a child.

De Lucía's technique was without peer — his right-hand tremolo, his picado (single-note runs), and his rasgueados (rhythmic strumming) set a standard that guitarists still aspire to today. But his true achievement was artistic: from the early 1970s onward, he began integrating elements of jazz, bossa nova, and Cuban music into flamenco, breaking the tradition's strict conventions and creating a new synthesis that was both deeply rooted and radically modern. His 1973 album Fuente y Caudal contained Entre dos Aguas, a rumba that became a pop hit across Spain and introduced flamenco guitar to a generation of listeners outside the Andalusian world.

His collaborations were as remarkable as his solo work: he performed regularly with classical guitarist John Williams and jazz guitarist Al Di Meola, and his partnership with flamenco singer Camarón de la Isla produced a series of albums in the 1970s that transformed flamenco from a folk tradition into a modern art form. His album Zyryab (1990), named after the 9th-century Arab musician who brought advanced music theory to Andalusia, is considered one of his masterpieces. De Lucía died suddenly of a heart attack in Mexico in 2014; he remains the defining standard against which all flamenco guitarists measure themselves.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Paco_de_Lucia_2009.jpg/440px-Paco_de_Lucia_2009.jpg",
    },
    "Tyagaraja": {
        "biography_short": "South Indian Carnatic music composer and devoted bhakta of Rama; one of the Trinity of Carnatic Music, he composed over 24,000 kritis — most of them personal devotional dialogues with his god.",
        "biography": """Tyagaraja (1767–1847) was a Telugu-language composer and one of the towering figures of Carnatic music — one of the three composers known as the Carnatic Trinity, alongside Muthuswami Dikshitar and Syama Sastri. Born in Thiruvarur, Tamil Nadu, and raised in Tiruvaiyaru on the banks of the Kaveri river, he was a devoted Vaishnava and bhakta (devotee) of Lord Rama, and virtually his entire musical output was an expression of this devotion.

Tyagaraja is credited with composing over 24,000 kritis, of which around 700 are in regular performance today. His kritis are distinctive for their combination of melodic beauty, rhythmic sophistication, and profound devotional lyric content — many are cast as direct personal addresses to Rama, ranging from joyful praise to tender petition to intimate questioning. He worked within the traditional raga and tala system but expanded its expressive range enormously, composing in a wide variety of ragas including many that he helped establish as major concert ragas.

His most celebrated works include the Pancharatna Kritis — five compositions in five different ragas that are traditionally performed together and are considered the summit of the Carnatic concert tradition. Tyagaraja resisted offers of royal patronage, preferring to live as an ascetic, going out daily to sing bhajans (devotional songs) and receiving food in return. He is said to have attained liberation at the age of 80, singing as he died. The annual Tyagaraja Aradhana festival held at Tiruvaiyaru, attended by thousands of musicians from across the world, celebrates his legacy every January.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Tyagaraja_swami.jpg/440px-Tyagaraja_swami.jpg",
    },
    "Muthuswami Dikshitar": {
        "biography_short": "One of the Carnatic Trinity, renowned for his erudite compositions combining deep Sanskrit scholarship with mastery of every raga; his kritis are the most harmonically rich in the Carnatic tradition.",
        "biography": """Muthuswami Dikshitar (1775–1835) was a South Indian composer and one of the Trinity of Carnatic Music. Born in Tiruvarur, Tamil Nadu, he received a thorough musical education under a Tantric scholar in Varanasi (Benares), where he also studied Sanskrit, astrology, and esoteric traditions. His years in the north exposed him to Hindustani music and to Western influences — he was one of the first Carnatic composers to incorporate Western notation and European melodic elements into kritis.

Dikshitar composed approximately 450–500 kritis, almost all of them in Sanskrit, and they are distinguished by their exceptional erudition: each composition typically encodes the raga's name (mudra), the tala, and often the presiding deity's iconographic details within the lyric itself — a form of textual complexity unique in the Carnatic repertoire. He composed in all 72 Melakarta ragas (the parent ragas of the Carnatic system), a feat of systematic completeness unmatched in the tradition.

His treatment of harmony is considered the most sophisticated of the Trinity: his compositions explore the full melodic and rhythmic possibilities of each raga with a depth and complexity that demands high musicianship to perform. The Navagraha Kritis (nine compositions dedicated to the nine celestial bodies of Hindu cosmology), the Navaavarana Kritis (dedicated to the nine enclosures of the Sri Chakra), and the Kamalamba Navavarana Kritis are considered his masterworks. Dikshitar spent much of his life on pilgrimage, composing kritis at temples across South India — many of the compositions encode the name and attributes of the deity at each specific shrine.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Muthuswami_Dikshitar.jpg/440px-Muthuswami_Dikshitar.jpg",
    },
    "Syama Sastri": {
        "biography_short": "The oldest of the Carnatic Trinity, known for the emotional depth and formal elegance of his compositions; his Navaratna Kritis in praise of the goddess Kamakshi are considered the summit of his art.",
        "biography": """Syama Sastri (1762–1827) was a Telugu-language Carnatic composer and the eldest of the Trinity of Carnatic Music. Born in Tiruvarur, Tamil Nadu, he was a contemporary and friend of Tyagaraja and a near-contemporary of Muthuswami Dikshitar. Like both his colleagues in the Trinity, he was a deeply religious man — his patron goddess was Kamakshi of Kanchipuram and Bangaru Kamakshi of Tiruvarur, and his compositions are infused with devotion and personal yearning.

Syama Sastri composed far fewer works than the other two members of the Trinity — only around 300 compositions survive — but they are prized for their elegance, emotional directness, and formal perfection. He excelled particularly at swarajati and varnam forms as well as kritis. His compositions in ragas such as Anandabhairavi, Bhairavi, Todi, and Saveri are considered definitive examples of those ragas' emotional character.

His most celebrated works are the Navaratna Kritis — nine compositions dedicated to the goddess Kamakshi in nine different ragas — which are considered among the most beautiful compositions in the Carnatic canon. Syama Sastri was also known for his unusual and sophisticated use of tala; he employed complex rhythmic structures including tisra gati (groups of three) and chatusra gati (groups of four) in ways that created rhythmic tension and resolution of great sophistication. He died at 65, leaving behind a relatively small but intensely refined body of work.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/Syama_Sastri.jpg/440px-Syama_Sastri.jpg",
    },
    "Tansen": {
        "biography_short": "The greatest musician of medieval India; court musician to Emperor Akbar and the founding figure of several Hindustani gharanas, credited with creating or refining numerous ragas still performed today.",
        "biography": """Tansen (c. 1506–1589) — also known as Miyan Tansen or Ramtanu Pandey — is the most celebrated musician in the history of Hindustani classical music and one of the nine jewels (Navaratnas) of Emperor Akbar's court at Fatehpur Sikri. Born in Gwalior, he studied under the great dhrupad singer Swami Haridas and the musician-saint Hazrat Muhammad Ghaus, and his early reputation grew so great that Akbar summoned him to his court, reportedly with great difficulty, in 1562.

Legends surrounding Tansen's abilities are extraordinary: he is said to have set a lamp ablaze by singing Raga Deepak and to have caused rain to fall by singing Raga Megh Malhar. While these accounts are mythological, they testify to the reverence in which he was held. As a historical figure, Tansen's influence on Hindustani music is immense and concrete: he is credited with creating or significantly developing numerous ragas, including Miyan ki Todi, Miyan ki Malhar, Miyan ki Sarang, and Darbari Kanada — all of which bear his informal title "Miyan" (lord) and remain major ragas in the contemporary concert repertoire.

Tansen was the progenitor of two of the most important gharanas (schools) of Hindustani classical music: the Senia Binkar Gharana (for sitar and surbahar) and the Senia Rabab Gharana (for rabab). His tomb in Gwalior, near his teacher Swami Haridas's hermitage, remains a pilgrimage site for musicians. The annual Tansen Music Festival (Tansen Samaroh) held at his tomb in Gwalior attracts the finest Hindustani classical musicians every November.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Tansen_Akbarnama.jpg/440px-Tansen_Akbarnama.jpg",
    },
    "Amir Khusrau": {
        "biography_short": "Persian-Indian poet, musician, and Sufi mystic credited with inventing qawwali and the sitar; the 'voice of India' synthesised Persian and Indian musical traditions as no one before or since.",
        "biography": """Amir Khusrau (1253–1325) was a Persian-Indian Sufi poet, musician, and scholar who is one of the most significant figures in the cultural history of the Indian subcontinent. Born Abul Hasan Yamīn ud-Dīn Khusrau in Patiyali (in present-day Uttar Pradesh) to a Turkic father and an Indian mother, he served at the courts of seven successive Delhi Sultanate rulers and was a devoted disciple of the Sufi mystic Hazrat Nizamuddin Auliya, whose dargah (shrine) in Delhi he is buried beside.

Khusrau is credited — though with varying degrees of historical certainty — with an extraordinary range of inventions and innovations in Indian music and language. He is traditionally held to be the originator of qawwali, the devotional musical form of the Chishti Sufi order that remains among the most powerful musical traditions in the world. He is also associated with the invention of the sitar (a modification of the veena) and the tabla (twin drums), and with the development of the khayal vocal form, though these attributions are debated among scholars.

His synthesis of Persian poetic forms with Indian musical structures created a bridge between the two great cultural spheres that met on the subcontinent, and his compositions in Braj Bhasha (an early form of Hindi) are considered among the earliest examples of literary Hindi. The tarana form — a rapid vocal composition using meaningless syllables — is attributed to him and remains a distinctive feature of Hindustani classical performance. Every year on the occasion of Basant (spring), qawwals gather at the Nizamuddin dargah in Delhi to sing his compositions in a tradition unbroken for seven centuries.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Amir_Khusro.jpg/440px-Amir_Khusro.jpg",
    },
    "Purandaradasa": {
        "biography_short": "15th-century Karnataka saint-composer known as the 'Father of Carnatic Music'; his systematisation of Carnatic music pedagogy and his thousands of devotional compositions laid the foundation of the entire tradition.",
        "biography": """Purandaradasa (c. 1484–1564) was a Karnataka-born saint, poet, and musician universally revered as the "Pitamaha" (grandfather) of Carnatic music for his foundational role in systematising its pedagogy. Born Srinivasa Nayaka in Kshemapura (present-day Karnataka), he was a wealthy merchant who, following a spiritual awakening, renounced his wealth and devoted himself entirely to the worship of Lord Vishnu through music, composing under the name Purandaradasa (servant of Purandara Vittala, a name of Krishna).

Purandaradasa's most lasting contribution was not any single composition but the creation of a systematic musical curriculum for Carnatic music: the graded series of exercises, varnams (etude-like pieces), and geetas (simple devotional songs) that he designed remain the foundation of Carnatic music education to this day. Every Carnatic music student begins with the exercises he devised — the sarali varisai (scale exercises), janta varisai (double-note exercises), and the simple devotional compositions he wrote for teaching purposes.

He is credited with composing over 475,000 compositions — an astronomical number that includes everything from simple teaching pieces to elaborate kritis — of which perhaps 1,000–2,000 survive in oral tradition. His compositions are written in Kannada, Sanskrit, and Telugu, and are infused with deep devotion and often sharp social commentary. He was associated with the philosopher-saint Vyasatirtha and with the Haridasa movement that used vernacular devotional music to spread Vaishnavism across Karnataka. The Purandarotsava festival, celebrating his legacy, is held annually across Karnataka.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Purandara_Dasa.jpg/440px-Purandara_Dasa.jpg",
    },
    "Swathi Thirunal": {
        "biography_short": "King of Travancore and prolific composer who wrote devotional and classical pieces in seven languages; his palace became a cultural center that brought Carnatic, Hindustani, and Western music together.",
        "biography": """Swathi Thirunal Rama Varma (1813–1846) was the Maharaja of Travancore (present-day Kerala) and one of the most gifted composer-patrons in the history of South Indian music. He ascended the throne at age 16 and reigned until his early death at 33, leaving behind an extraordinary body of musical compositions and transforming the Travancore palace into the cultural centre of South India.

Swathi Thirunal composed approximately 400 works in seven languages — Malayalam, Sanskrit, Telugu, Hindi, Kannada, Marathi, and Tamil — spanning both Carnatic and Hindustani traditions. He was extraordinarily well-versed in both classical systems, and his compositions reflect the cultural crossroads that Travancore represented. His famous Navaratri Kritis — nine compositions in Sanskrit dedicated to the goddess Saraswati, one for each day of the Navaratri festival — are performed annually at the Padmanabhapuram palace as part of a tradition he established.

Beyond composition, Swathi Thirunal was a remarkable patron who invited the greatest musicians of his time to his court: the legendary singer Shadkala Govinda Marar was his court musician, and Swathi Thirunal studied under some of the finest Carnatic masters. He also integrated Western instruments into the palace orchestra and wrote compositions for them — an unusual and forward-looking synthesis for the 1830s. Several of his compositions were thought lost until manuscripts were discovered in the palace archives in the 1960s, triggering a major revival of interest. The Swathi Music Festival, held annually in Thiruvananthapuram, celebrates his legacy.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Swathi_Thirunal.jpg/440px-Swathi_Thirunal.jpg",
    },
    "Abu Nasr al-Farabi": {
        "biography_short": "Medieval Islamic philosopher and music theorist whose Grand Book of Music systematised the maqam scales and instruments of the Islamic world; 'The Second Teacher' after Aristotle.",
        "biography": """Abu Nasr Muhammad al-Farabi (c. 872–950) — known in the West as Alpharabius — was a medieval Islamic philosopher, music theorist, mathematician, and cosmologist, regarded as one of the greatest scholars of the early Islamic Golden Age. Born in Farab (in modern Kazakhstan or Turkmenistan) of Turkic origin, he spent most of his productive life in Baghdad and later at the court of the Hamdanid ruler Sayf al-Dawla in Aleppo, where he died.

Al-Farabi earned the honorific "Second Teacher" (al-Mu'allim al-Thani) — Aristotle being the first — for his comprehensive commentaries on and extensions of Aristotelian logic, metaphysics, and political philosophy. His musical contributions are equally foundational: his Kitab al-Musiqa al-Kabir (Grand Book of Music) is the most comprehensive treatise on music theory produced in the medieval Islamic world. In it, he systematised the maqam scale system, described the acoustical properties of musical instruments, theorised the relationships between intervals, and laid out the principles of rhythm and meter in Islamic music.

Al-Farabi was himself a skilled practitioner: medieval accounts credit him with playing the oud with extraordinary skill and inventing the qanun (zither). His theoretical framework — linking music to mathematics, natural philosophy, and the human soul — was enormously influential on subsequent Islamic music theory and, through Latin translations, on medieval European musical thought. His work on the classification of musical modes directly influenced the systematisation of the maqam tradition that remains central to Arabic, Turkish, and Persian classical music.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Al-Farabi.jpg/440px-Al-Farabi.jpg",
    },
    "Ziryab": {
        "biography_short": "9th-century Arab musician who transformed Andalusian culture after his arrival in Córdoba; added a fifth string to the oud, founded the first music conservatory in Europe, and established standards of taste still felt today.",
        "biography": """Ziryab (789–857) — full name Abu l-Hasan ʿAlī ibn Nāfiʿ — was an Arab musician, singer, composer, and polymath of extraordinary cultural influence who transformed the court of Córdoba under Abd al-Rahman II into one of the great centres of Islamic and European civilisation. Born in Baghdad to a family of African origin, he studied at the Abbasid court under the master oud player Ishaq al-Mawsili, whose jealousy at his student's superior gifts forced Ziryab to flee west to Andalusia.

At the Umayyad court of Córdoba, Ziryab became the supreme arbiter of music, culture, and taste. His musical innovations were lasting: he added a fifth string to the traditional four-string oud, reportedly using an eagle's talon as a plectrum, giving the instrument greater range and expression. He founded what is considered the first music conservatory in the Western world, teaching a systematic approach to musical education that influenced Andalusian music for centuries. He is credited with composing hundreds of nawbat — suites of songs in specific modes for different times of day, a tradition that evolved into the Andalusian nuba form still performed in North Africa today.

Beyond music, Ziryab transformed Andalusian court culture in ways that still resonate: he introduced the concept of seasonal fashion (changing clothes with the season), established new standards of personal hygiene, introduced toothpaste and deodorant to Andalusian courts, popularised the asparagus as a food, and redesigned the formal dinner into multiple courses. His name — which means "blackbird" in Arabic, referring to his dark complexion and beautiful voice — became synonymous in medieval sources with elegance, refinement, and creative genius.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Ziryab.jpg/440px-Ziryab.jpg",
    },
    "Safi al-Din al-Urmawi": {
        "biography_short": "13th-century Persian music theorist who systematised the Arabic-Persian maqam system; his Kitab al-Adwar established the theoretical framework for Islamic art music that persisted for centuries.",
        "biography": """Safi al-Din Abd al-Mumin al-Urmawi (c. 1216–1294) was a Persian music theorist, calligrapher, and court musician who served the last Abbasid caliphs in Baghdad and became the most influential theorist of the Arabic-Persian maqam system in the medieval period. Born in Urmia (in present-day northwestern Iran), he rose to become chief librarian and court musician to the Abbasid Caliph al-Mustasim — the last caliph before the Mongol destruction of Baghdad in 1258.

Remarkably, al-Urmawi survived the Mongol conquest, which killed the caliph and destroyed most of the library, and continued his scholarly work under the Ilkhanid Mongol rulers. His two major treatises — Kitab al-Adwar (Book of Musical Cycles) and Risala al-Sharafiyya — are the foundational theoretical documents of medieval Arabic-Persian music theory. In the Kitab al-Adwar, he systematised the 17-tone scale system, defined the principal maqamat (modal scales) and their emotional characters, and described the rhythmic cycles (iqa'at) used in Arabic musical practice.

His theoretical framework — building on al-Farabi and the earlier Arabic music theorists while incorporating Persian and Greek sources — provided the conceptual vocabulary for Arabic, Persian, and Ottoman music theory for the next several centuries. The scale system he formalised, dividing the octave into 17 intervals based on Pythagorean ratios, influenced not only Islamic music but, through later Ottoman theorists, the development of Turkish makam music. Al-Urmawi is also known for his extraordinary calligraphy; examples of his script survive in Istanbul and are considered masterworks of the art.""",
        "image_url": "",
    },
    "Hammamizade İsmail Dede Efendi": {
        "biography_short": "The greatest composer of Ottoman classical music; his 600 surviving compositions — fasıls, ilahis, and şarkıs — defined the golden age of the makam tradition in Istanbul.",
        "biography": """Hammamizade İsmail Dede Efendi (1778–1846) was an Ottoman Turkish composer who is universally regarded as the greatest composer in the history of Ottoman classical music. Born in Istanbul, he received his musical education at the Ottoman palace and studied composition under the master musician Uncuzade Salih Efendi. He later became a dervish of the Mevlevi (Whirling Dervish) order — the Sufi order that was the primary institutional home of Ottoman musical culture — and composed extensively for the Mevlevi sema (ceremonial turning) ritual.

Dede Efendi composed over 600 works — approximately 300 are known to survive — spanning the full range of Ottoman classical genres: fasıl (a multi-section suite in a single makam), ilahi (devotional hymn), na't (praise of the Prophet), şarkı (secular art song), and sema pieces for the Mevlevi ceremony. He worked in virtually all of the principal makamlar (modal scales) of the Ottoman system, and his compositions are noted for their architectural perfection, melodic inventiveness, and emotional depth.

His Segâh Fasıl is considered one of the supreme achievements of Ottoman music — a multi-movement suite in the melancholy Segâh makam that builds from gentle opening movements to a deeply moving conclusion. He also composed in the Hicaz makam, associated with longing and spiritual yearning, with particular mastery. Dede Efendi spent the final years of his life in Mecca after performing the Hajj, and died there. His legacy is preserved and performed by the Istanbul State Turkish Music Ensemble and by conservatories across Turkey and the Middle East.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Hammamizade_%C4%B0smail_Dede_Efendi.jpg/440px-Hammamizade_%C4%B0smail_Dede_Efendi.jpg",
    },
    "Alladiya Khan": {
        "biography_short": "Legendary khayal vocalist and founder of the Jaipur-Atrauli gharana; his complex, ornate style — emphasising the full elaboration of a raga over hours — defined one of the most demanding schools in Hindustani music.",
        "biography": """Alladiya Khan (1855–1946) was an Indian classical vocalist of the Hindustani tradition and one of the most revered figures in the history of khayal singing. Born in Atrauli (in present-day Uttar Pradesh) into a musical family, he trained under his father and uncle before developing a unique vocal style that would eventually establish the Jaipur-Atrauli gharana — one of the four major gharanas (schools) of khayal singing.

The Jaipur-Atrauli style that Alladiya Khan systematised and transmitted is distinguished by its commitment to slow, elaborate, and deeply ornate raga development. Where other gharanas prioritise the beauty of the melody or the sweetness of tone, the Jaipur-Atrauli approach emphasises the grammar and logic of the raga itself — the precise hierarchy of notes, the specific ornaments (gamakas) appropriate to each raga, and the patient, disciplined unfolding of the raga's character over many hours. The vilambit (slow tempo) khayal in this tradition can last an hour or more, with the vocalist exploring every nuance of the raga before introducing the bandish (composed piece).

Alladiya Khan lived to the extraordinary age of 91, performing and teaching until late in his life. His disciples included his sons Manji Khan and Bhurji Khan, and through them and their students his lineage has continued into the present generation. Singers like Kishori Amonkar, Shruti Sadolikar, and Mallikarjun Mansur are among those who carry the Jaipur-Atrauli tradition, with its characteristic combination of rigour, complexity, and authority.""",
        "image_url": "",
    },
    "Vishnu Digambar Paluskar": {
        "biography_short": "Indian classical vocalist who democratised Hindustani music by performing it in public for all castes, founded the landmark Gandharva Mahavidyalaya music school, and brought classical music out of the courts.",
        "biography": """Vishnu Digambar Paluskar (1872–1931) was an Indian classical vocalist and music educator who played a pivotal role in transforming Hindustani classical music from a courtly tradition, jealously guarded by hereditary musicians, into a publicly accessible art form. Born in Kurundwad (in present-day Maharashtra) into a non-musician family, he lost his sight in an accident at the age of ten and was sent to study music under Balkrishnabuwa Ichalkaranjikar, a master of the Gwalior gharana.

Paluskar's revolutionary contribution was institutional and social as much as artistic. In 1901, he founded the Gandharva Mahavidyalaya (Academy of Heavenly Music) in Lahore — the first school to teach Hindustani classical music on a systematic, institutional basis, open to students of all castes and backgrounds. Previously, classical music had been taught within hereditary families under a system of strict secrecy; Paluskar's school represented a fundamental break with this tradition, creating a model that was replicated across India as branches of the Mahavidyalaya opened in Bombay, Pune, and other cities.

He was also a fervent nationalist who integrated classical music into the independence movement: he sang at Congress sessions, composed songs in praise of Ram and the nation, and made Hindustani music a vehicle for national cultural pride. His bhajan (devotional song) Raghupati Raghava Raja Ram became one of the most sung songs of the independence movement and remains iconic. Paluskar trained hundreds of students who went on to become leading musicians and teachers; his institutional legacy is arguably as important as his musical one.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Vishnu_Digambar_Paluskar.jpg/440px-Vishnu_Digambar_Paluskar.jpg",
    },
    "Vishnu Narayan Bhatkhande": {
        "biography_short": "Indian musicologist who systematised Hindustani classical music by creating the 10-thaat classification, writing down hundreds of ragas and bandishes, and establishing a standardised notation system.",
        "biography": """Vishnu Narayan Bhatkhande (1860–1936) was an Indian musicologist, lawyer, and music educator who undertook the most comprehensive systematic study and documentation of Hindustani classical music of the modern era. Born in Bombay into a Brahmin family, he trained as a lawyer but devoted his life to music scholarship, travelling across India for decades to study with hundreds of musicians from different gharanas and regions.

Bhatkhande's central problem was the chaotic and fragmented state of Hindustani music theory in the early twentieth century: different gharanas used different terminologies, different raga classifications, and passed down their knowledge orally with no standardised system. His solution was systematic research and codification. His major work, Hindustani Sangeet Paddhati (System of Hindustani Music, 4 volumes), documented over 1,800 bandishes (compositions) in hundreds of ragas, with standard notation using the system he developed — a modified sargam notation that became the standard for written Hindustani music.

His most lasting contribution was the classification of all Hindustani ragas into ten parent scales called thaats — Kalyan, Bilawal, Khamaj, Bhairav, Poorvi, Marwa, Kafi, Asavari, Bhairavi, and Todi — a system that is still the basis of Hindustani music pedagogy today. He founded important music schools including the Marris College of Music in Lucknow (now Bhatkhande Music Institute University) and the Madhav Music College in Gwalior. His work, though sometimes criticised for reducing the fluid oral tradition to rigid categories, gave Hindustani music the systematic theoretical foundation it needed to survive and flourish in the modern world.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Vishnu_Narayan_Bhatkhande.jpg/440px-Vishnu_Narayan_Bhatkhande.jpg",
    },
    "Papanasam Sivan": {
        "biography_short": "Tamil composer and lyricist called the 'Carnatic Thyagaraja of Tamil'; composed over 500 devotional songs in Tamil and other languages that brought Carnatic music to Tamil-speaking audiences.",
        "biography": """Papanasam Sivan (1890–1973) — born Ramiah Iyer — was a Tamil composer, vocalist, and music teacher widely regarded as one of the greatest composers to have written Carnatic music in the Tamil language. Born in Porayar, Tamil Nadu, he was a child prodigy who performed in public at age seven and studied under several Carnatic masters. He later worked extensively in the Tamil film industry, composing music for over 100 Tamil films during the golden age of Tamil cinema and becoming one of the most recognisable names in Tamil cultural life.

Papanasam Sivan's contribution to Carnatic music was to bring it to Tamil-speaking devotees in their own language. The traditional Carnatic Trinity — Tyagaraja, Dikshitar, and Syama Sastri — had composed primarily in Telugu and Sanskrit, and while their music was deeply respected, the language barrier limited its accessibility for Tamil audiences. Sivan composed over 500 kritis in Tamil, as well as compositions in Telugu, Sanskrit, Malayalam, and Kannada, creating a body of work that made Carnatic devotional music available to Tamil speakers in their mother tongue.

His compositions are marked by their melodic accessibility, strong literary quality — he was as much a poet as a musician — and deep devotional feeling. He composed in honour of deities across the Tamil Hindu tradition, from Murugan and Ganesha to Shiva and Vishnu. His film songs, many of which were set to classical ragas, brought Carnatic melodic sensibility to mainstream Tamil audiences and remain beloved classics. He received the Sangita Kalanidhi award from the Music Academy of Madras, the highest honour in Carnatic music, in 1944.""",
        "image_url": "",
    },
    "Sunjata Keita": {
        "biography_short": "13th-century founder of the Mali Empire, celebrated in the Griot oral tradition as a heroic king whose life story — the Sundiata Epic — is sung in praise across West Africa to this day.",
        "biography": """Sunjata Keita (c. 1217–1255) was the founder and first Mansa (emperor) of the Mali Empire, one of the great pre-colonial states of West Africa. Born into the ruling Keita clan of the Mandinka people, he is remembered as a semi-legendary figure whose life — including his miraculous recovery from childhood disability, his years of exile, and his ultimate victory over the Sosso king Sumanguru Kante at the Battle of Kirina (c. 1235) — forms the basis of the Sundiata Epic, one of the most celebrated oral traditions in Africa.

Sunjata's relationship to music and musical culture is inseparable from the Griot tradition. The Griots (djeli in Mande languages) are hereditary musician-historians who serve noble families, preserving and transmitting history, genealogy, and wisdom through song, narration, and the playing of the kora, balafon, and other instruments. Sunjata's court included the master Griot Balla Fasséké, and the relationship between king and Griot — one holding political power, the other holding cultural memory — is a fundamental structure of Mande society.

The Sundiata Epic, performed by Griots across the Mande-speaking world from Guinea to Mali to Senegal, is not a fixed text but a living tradition: each Griot performance is an improvisation within a known structure, with the performer drawing on his family's version of the story, his own poetic gifts, and his responsiveness to the audience. The kora — a 21-string bridge-harp — and the balafon (a wooden xylophone) are the principal instruments of these performances. Sunjata's story is thus not merely history but the foundation of a living musical and cultural tradition that continues to evolve in the twenty-first century.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Sundjata_keita.jpg/440px-Sundjata_keita.jpg",
    },
    "Joseph Haydn": {
        "biography_short": "Austrian composer known as the 'Father of the Symphony' and 'Father of the String Quartet'; his 104 symphonies and 68 string quartets established the forms that defined classical music for generations.",
        "biography": """Joseph Haydn (1732–1809) was an Austrian composer of the Classical period, known as the "Father of the Symphony" and "Father of the String Quartet" for his decisive role in establishing these forms as the central vehicles of classical instrumental music. Born in Rohrau, Lower Austria, the son of a wheelwright, he was a chorister at St Stephen's Cathedral in Vienna as a boy before embarking on a career that would make him the most celebrated living composer in Europe.

For nearly thirty years (1761–1790), Haydn served as Kapellmeister at the Esterházy estate — first at Eisenstadt, then at the grand palace of Eszterháza in Hungary — for the wealthy Esterházy princes, who maintained a permanent orchestra, opera house, and puppet theatre. This long, settled employment gave Haydn an unparalleled laboratory for musical experimentation: he could try out ideas immediately with his own orchestra, observe the results, and refine his technique. His 104 numbered symphonies, composed over several decades, trace the evolution from elegant entertainment to the profound late works — the twelve "London" symphonies, composed for Haydn's triumphant visits to England in 1791–92 and 1794–95, are among the greatest orchestral works of the eighteenth century.

His 68 string quartets, above all the six quartets of Op. 76 (1797–1799), established the conversation between four equal voices as the quintessential chamber music form. His two late oratorios — The Creation (1798) and The Seasons (1801) — were enormously popular in his lifetime and remain among the most performed choral works of the period. Haydn was a friend and mentor to the young Mozart, and taught the young Beethoven. Serene, good-humoured, and deeply religious, he represents in many ways the ideal of the Classical style: elegant, balanced, witty, and humane.""",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Joseph_Haydn_portrait_by_Thomas_Hardy_%28small%29.jpg/440px-Joseph_Haydn_portrait_by_Thomas_Hardy_%28small%29.jpg",
    },
}

# ---------------------------------------------------------------------------
# Additional compositions for composers with zero or few compositions
# ---------------------------------------------------------------------------

ADDITIONAL_COMPOSITIONS = [
    # --- Ziryab ---
    {
        "composer_wikidata": "Q313275",
        "title": "Nawba al-Ramal",
        "title_native": "نوبة الرمل",
        "composition_type": "maqam",
        "tradition_name": "Maqam (Arabic)",
        "description": "A ceremonial suite in the Ramal mode, attributed to Ziryab's Andalusian school. The nawba (nuba) form he systematised evolved into the foundational suite tradition of Andalusian-Moroccan classical music.",
        "language": "Arabic",
        "year_composed": 830,
    },
    # --- Abu Nasr al-Farabi ---
    {
        "composer_wikidata": "Q41085",
        "title": "Melodic Exercises from the Grand Book of Music",
        "title_native": "من كتاب الموسيقى الكبير",
        "composition_type": "maqam",
        "tradition_name": "Maqam (Arabic)",
        "description": "Melodic demonstrations composed by al-Farabi to illustrate the modal system described in his Kitab al-Musiqa al-Kabir. These short pieces served as theoretical examples demonstrating the emotional qualities of each maqam.",
        "language": "Arabic",
        "year_composed": 940,
    },
    # --- Safi al-Din al-Urmawi ---
    {
        "composer_wikidata": "Q713338",
        "title": "Rawdhat al-Fusul wa Ghayat al-Amal",
        "title_native": "روضة الفصول وغاية الآمل",
        "composition_type": "maqam",
        "tradition_name": "Maqam (Arabic)",
        "description": "A theoretical composition demonstrating the 12 primary maqamat systematised by al-Urmawi in his Kitab al-Adwar. One of the earliest surviving compositions in the codified Arabic maqam tradition.",
        "language": "Arabic",
        "year_composed": 1270,
    },
    # --- Alladiya Khan ---
    {
        "composer_wikidata": "Q4730042",
        "title": "Jaunpuri Bada Khayal — Piya Bin Nahin Aavat Chain",
        "title_native": "पिया बिन नहीं आवत चैन",
        "composition_type": "khayal",
        "tradition_name": "Hindustani Classical",
        "description": "A bada (slow) khayal in Raga Jaunpuri, one of the signature compositions of the Jaipur-Atrauli gharana. The composition exemplifies the gharana's emphasis on deep raga elaboration, complex ornaments, and the slow, meditative unfolding of the raga's character.",
        "language": "Hindi/Braj Bhasha",
        "year_composed": None,
    },
    # --- Vishnu Digambar Paluskar ---
    {
        "composer_wikidata": "Q3556547",
        "title": "Raghupati Raghava Raja Ram",
        "title_native": "रघुपति राघव राजा राम",
        "composition_type": "bhajan",
        "tradition_name": "Hindustani Classical",
        "description": "A bhajan in praise of Lord Rama that Paluskar popularised and that became one of the most widely sung songs of the Indian independence movement. Mahatma Gandhi's favourite prayer song, it was sung at Congress sessions and protests across India.",
        "language": "Sanskrit/Hindi",
        "year_composed": 1915,
    },
    # --- Vishnu Narayan Bhatkhande ---
    {
        "composer_wikidata": "Q1339065",
        "title": "Yaman Kalyan Bandish — Eri Aali Piya Bin",
        "title_native": "एरी आली पिया बिन",
        "composition_type": "khayal",
        "tradition_name": "Hindustani Classical",
        "description": "A vilambit (slow) khayal in Raga Yaman Kalyan, one of the teaching compositions included in Bhatkhande's Hindustani Sangeet Paddhati. Written as a pedagogical example of the Yaman Kalyan raga, it is widely used in music education across North India.",
        "language": "Braj Bhasha",
        "year_composed": 1910,
    },
    # --- Papanasam Sivan ---
    {
        "composer_wikidata": "Q1053012",
        "title": "Bhavayami Raghuramam",
        "title_native": "பவயாமி ரகுராமம்",
        "composition_type": "kriti",
        "tradition_name": "Carnatic Classical",
        "description": "A Tamil-language kriti in Raga Mohanam dedicated to Lord Rama. One of Papanasam Sivan's most beloved compositions, exemplifying his gift for melodic accessibility and strong lyrical content in Tamil — his mission to bring Carnatic music to Tamil-speaking devotees.",
        "language": "Tamil",
        "year_composed": 1940,
    },
    # --- Vivaldi — add more ---
    {
        "composer_wikidata": "Q1340",
        "title": "Gloria in D major",
        "title_native": "Gloria RV 589",
        "composition_type": "oratorio",
        "tradition_name": "Western Classical",
        "description": "One of Vivaldi's most celebrated sacred choral works, composed for the Ospedale della Pietà in Venice. A joyful, accessible setting of the Gloria text from the Mass, it is today one of the most performed Baroque choral pieces.",
        "language": "Latin",
        "year_composed": 1715,
    },
    # --- Handel — add more ---
    {
        "composer_wikidata": "Q7302",
        "title": "Water Music Suites",
        "title_native": None,
        "composition_type": "suite",
        "tradition_name": "Western Classical",
        "description": "Three orchestral suites composed for a royal water pageant on the River Thames in July 1717, attended by King George I. The music — for winds, strings, and brass — was performed on a barge following the royal boat, and the king enjoyed it so much he reportedly requested it repeated three times.",
        "language": None,
        "year_composed": 1717,
    },
    # --- Haydn ---
    {
        "composer_wikidata": "Q7349",
        "title": "The Creation",
        "title_native": "Die Schöpfung",
        "composition_type": "oratorio",
        "tradition_name": "Western Classical",
        "description": "Haydn's monumental oratorio depicting the creation of the world, based on texts from Genesis and Milton's Paradise Lost. Premiered in Vienna in 1798 and instantly celebrated as his masterpiece, it remains one of the most performed oratorios in the choral repertoire.",
        "language": "German",
        "year_composed": 1798,
    },
    # --- Paganini ---
    {
        "composer_wikidata": "Q168701",
        "title": "Violin Concerto No. 1 in D major",
        "title_native": None,
        "composition_type": "concerto",
        "tradition_name": "Western Classical",
        "description": "Paganini's first violin concerto, composed around 1817–18. A showpiece of extraordinary difficulty and brilliance, its final movement (Rondo) in particular demands left-hand pizzicato, rapid double-stops, and stratospheric high notes. The definitive Romantic-era virtuoso concerto before Mendelssohn.",
        "language": None,
        "year_composed": 1818,
    },
]


def run_sql(sql: str) -> None:
    db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:uzGvKmjbUjIrpeBbTzfQhnLzheFbashG@ballast.proxy.rlwy.net:10439/railway")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".sql", delete=False) as f:
        f.write(sql)
        fname = f.name
    result = subprocess.run(
        ["psql", db_url, "-f", fname, "-v", "ON_ERROR_STOP=1"],
        capture_output=True, text=True
    )
    os.unlink(fname)
    if result.returncode != 0:
        print("STDERR:", result.stderr[:2000])
        sys.exit(1)
    print(result.stdout[:500] if result.stdout else "(ok)")


def escape(s: str | None) -> str:
    if s is None:
        return "NULL"
    return "'" + s.replace("'", "''") + "'"


def main():
    print("=== Updating composer biographies ===")

    update_parts = []
    for name, data in BIOGRAPHIES.items():
        bio = escape(data.get("biography", ""))
        bio_short = escape(data.get("biography_short", ""))
        image = escape(data.get("image_url", ""))
        update_parts.append(
            f"  UPDATE composers SET "
            f"biography = {bio}, "
            f"biography_short = {bio_short}, "
            f"image_url = {image} "
            f"WHERE name = {escape(name)};"
        )

    sql = "\n".join(update_parts)
    run_sql(sql)
    print(f"Updated {len(BIOGRAPHIES)} composer biographies.")

    print("\n=== Adding additional compositions ===")

    comp_parts = []
    for c in ADDITIONAL_COMPOSITIONS:
        comp_type = escape(c.get("composition_type"))
        year = str(c["year_composed"]) if c.get("year_composed") else "NULL"
        lang = escape(c.get("language"))
        desc = escape(c.get("description"))
        title_native = escape(c.get("title_native"))

        comp_parts.append(f"""
  INSERT INTO compositions (id, title, title_native, composer_id, tradition_id, composition_type, language, description, year_composed, created_at, updated_at)
  SELECT
    gen_random_uuid(),
    {escape(c['title'])},
    {title_native},
    (SELECT id FROM composers WHERE wikidata_id = {escape(c['composer_wikidata'])} LIMIT 1),
    (SELECT id FROM musical_traditions WHERE name = {escape(c['tradition_name'])} LIMIT 1),
    {comp_type},
    {lang},
    {desc},
    {year},
    NOW(), NOW()
  WHERE
    NOT EXISTS (
      SELECT 1 FROM compositions
      WHERE title = {escape(c['title'])}
        AND composer_id = (SELECT id FROM composers WHERE wikidata_id = {escape(c['composer_wikidata'])} LIMIT 1)
    )
    AND (SELECT id FROM composers WHERE wikidata_id = {escape(c['composer_wikidata'])} LIMIT 1) IS NOT NULL;
""")

    run_sql("\n".join(comp_parts))
    print(f"Added up to {len(ADDITIONAL_COMPOSITIONS)} additional compositions.")

    print("\nDone!")


if __name__ == "__main__":
    main()
