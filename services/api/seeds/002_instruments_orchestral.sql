-- ── Update existing records that have museum-item descriptions ────────────────
UPDATE instruments SET
  hs_category      = 'Chordophone',
  hornbostel_sachs = '321.322-71',
  description      = 'The soprano instrument of the violin family and the most widely used orchestral string instrument. Developed in 16th-century Italy, it has four strings tuned in perfect fifths (G-D-A-E).',
  origin_region    = 'Western Europe',
  wikipedia_slug   = 'Violin',
  updated_at       = now()
WHERE name = 'Violin';

UPDATE instruments SET
  hs_category      = 'Chordophone',
  hornbostel_sachs = '321.322-71',
  description      = 'The bass instrument of the violin family, also called the cello. Has four strings (C-G-D-A) and produces a rich, warm tone in the tenor and bass registers. Central to chamber and orchestral music.',
  origin_region    = 'Western Europe',
  wikipedia_slug   = 'Cello',
  updated_at       = now()
WHERE name = 'Violoncello';

UPDATE instruments SET
  hs_category      = 'Chordophone',
  hornbostel_sachs = '321.322-71',
  description      = 'The largest and lowest-pitched instrument of the violin family. The foundation of the orchestral string section, tuned a major second lower than a cello.',
  origin_region    = 'Western Europe',
  wikipedia_slug   = 'Double_bass',
  updated_at       = now()
WHERE name = 'Double bass';

UPDATE instruments SET
  hs_category      = 'Aerophone',
  hornbostel_sachs = '421.121.12',
  description      = 'A cylindrical side-blown woodwind instrument. One of the most versatile orchestral instruments, capable of expressing a wide range of emotions from lyrical song to rapid virtuosic passages.',
  origin_region    = 'Western Europe',
  wikipedia_slug   = 'Western_concert_flute',
  updated_at       = now()
WHERE name = 'Flute';

UPDATE instruments SET
  hs_category      = 'Aerophone',
  hornbostel_sachs = '423.232',
  description      = 'A natural coiled brass instrument. In the orchestra, the French horn (or horn) bridges the brass and woodwind sections with a warm, mellow tone capable of both power and delicacy.',
  origin_region    = 'Western Europe',
  wikipedia_slug   = 'French_horn',
  updated_at       = now()
WHERE name = 'Horn';

UPDATE instruments SET
  hs_category      = 'Aerophone',
  hornbostel_sachs = '423.21',
  description      = 'A brass instrument with a cylindrical bore and a slide mechanism to change pitch. Foundational to the orchestral brass section and jazz music.',
  origin_region    = 'Western Europe',
  wikipedia_slug   = 'Trombone',
  updated_at       = now()
WHERE name = 'Trombone';

UPDATE instruments SET
  hs_category      = 'Aerophone',
  hornbostel_sachs = '423.233',
  description      = 'A valved brass instrument with a bright, penetrating tone. The highest-pitched standard orchestral brass instrument, it plays a leading role in both classical and jazz music.',
  origin_region    = 'Western Europe',
  wikipedia_slug   = 'Trumpet',
  updated_at       = now()
WHERE name = 'Trumpet';

UPDATE instruments SET
  hs_category      = 'Chordophone',
  hornbostel_sachs = '322.221',
  description      = 'A large concert harp with 47 strings spanning 6.5 octaves and 7 pedals allowing all keys. The orchestral harp is the only standard orchestral instrument with a pedal mechanism for chromaticism.',
  origin_region    = 'Western Europe',
  wikipedia_slug   = 'Harp',
  updated_at       = now()
WHERE name = 'Harp';

UPDATE instruments SET
  hs_category      = 'Chordophone',
  hornbostel_sachs = '314.122-4-8',
  description      = 'A keyboard instrument in which hammers strike strings. The modern concert grand piano has 88 keys spanning over 7 octaves. Arguably the most versatile instrument in Western classical music.',
  origin_region    = 'Western Europe',
  wikipedia_slug   = 'Piano',
  updated_at       = now()
WHERE name = 'Piano';

-- ── Insert missing orchestral instruments ─────────────────────────────────────
INSERT INTO instruments (id, name, name_native, hs_category, hornbostel_sachs, description, origin_region, materials, wikipedia_slug, created_at, updated_at)
VALUES

-- Strings
(gen_random_uuid(), 'Viola', NULL, 'Chordophone', '321.322-71',
 'The alto member of the violin family, tuned a fifth below the violin (C-G-D-A). Slightly larger than a violin with a deeper, warmer tone. Plays inner voices in orchestral and chamber music.',
 'Western Europe', ARRAY['spruce','maple','ebony'], 'Viola', now(), now()),

(gen_random_uuid(), 'Cello', NULL, 'Chordophone', '321.322-71',
 'The tenor-bass member of the violin family, played upright between the legs with an endpin. Four strings tuned C-G-D-A. Known for its singing, vocal quality and enormous dynamic range.',
 'Western Europe', ARRAY['spruce','maple','ebony'], 'Cello', now(), now()),

(gen_random_uuid(), 'Contrabass', NULL, 'Chordophone', '321.322-71',
 'Alternative name for the double bass — the lowest-pitched bowed string instrument in the modern symphony orchestra. Provides the harmonic and rhythmic foundation of the string section.',
 'Western Europe', ARRAY['spruce','maple'], 'Double_bass', now(), now()),

-- Woodwinds
(gen_random_uuid(), 'Piccolo', 'Flauto piccolo', 'Aerophone', '421.121.12',
 'The smallest and highest-pitched woodwind instrument in the orchestra, sounding one octave above the concert flute. Its penetrating tone cuts through the full orchestra.',
 'Western Europe', ARRAY['grenadilla wood','silver','nickel'], 'Piccolo', now(), now()),

(gen_random_uuid(), 'Oboe', NULL, 'Aerophone', '422.112',
 'A conical-bore double-reed woodwind with a distinctive penetrating, nasal tone. The oboe gives the tuning note (A) to the orchestra before concerts. Its tone is sometimes described as plaintive and expressive.',
 'Western Europe', ARRAY['grenadilla wood','metal keys'], 'Oboe', now(), now()),

(gen_random_uuid(), 'Cor Anglais', 'Corno inglese', 'Aerophone', '422.112',
 'The alto oboe, also called English horn. A double-reed woodwind a fifth lower than the oboe, with a bulbous bell giving it a haunting, melancholic tone. Famous solos in Dvořák''s New World Symphony.',
 'Western Europe', ARRAY['grenadilla wood','metal'], 'Cor_anglais', now(), now()),

(gen_random_uuid(), 'Clarinet', NULL, 'Aerophone', '422.211.2',
 'A single-reed cylindrical-bore woodwind available in several sizes. The B♭ clarinet is standard in orchestras. Known for its extraordinarily wide dynamic and expressive range — from whisper to full power.',
 'Western Europe', ARRAY['grenadilla wood','metal keys'], 'Clarinet', now(), now()),

(gen_random_uuid(), 'Bass Clarinet', NULL, 'Aerophone', '422.211.2',
 'A low-pitched clarinet sounding an octave below the B♭ clarinet. Has a distinctive upturned bell and neck crook. Provides a dark, resonant bass voice in the woodwind section.',
 'Western Europe', ARRAY['grenadilla wood','metal'], 'Bass_clarinet', now(), now()),

(gen_random_uuid(), 'Bassoon', NULL, 'Aerophone', '422.112',
 'The bass woodwind of the double-reed family. Its long, doubled-back conical tube gives a warm, rich bassoon tone spanning three octaves. Often called the "clown of the orchestra" for its comic possibilities.',
 'Western Europe', ARRAY['maple','bocal metal'], 'Bassoon', now(), now()),

(gen_random_uuid(), 'Contrabassoon', 'Contrafagotto', 'Aerophone', '422.112',
 'The lowest-pitched woodwind instrument in the symphony orchestra, sounding one octave below the bassoon. Its enormous doubled tube (over 5 metres unfolded) produces a dark, growling bass tone.',
 'Western Europe', ARRAY['maple','metal'], 'Contrabassoon', now(), now()),

(gen_random_uuid(), 'Soprano Saxophone', NULL, 'Aerophone', '422.212',
 'The highest-pitched common saxophone, usually straight-bodied. Used in orchestral, jazz, and contemporary music.',
 'Western Europe', ARRAY['brass','metal keys'], 'Soprano_saxophone', now(), now()),

(gen_random_uuid(), 'Alto Saxophone', NULL, 'Aerophone', '422.212',
 'The most common saxophone, curved with a range from D♭3 to A♭5. The standard instrument for classical saxophone concertos and jazz improvisation.',
 'Western Europe', ARRAY['brass','metal keys'], 'Alto_saxophone', now(), now()),

(gen_random_uuid(), 'Tenor Saxophone', NULL, 'Aerophone', '422.212',
 'A B♭ saxophone with a rich, full-bodied tone central to jazz music. One octave lower than the soprano, with the iconic curved neck and body.',
 'Western Europe', ARRAY['brass','metal keys'], 'Tenor_saxophone', now(), now()),

(gen_random_uuid(), 'Baritone Saxophone', NULL, 'Aerophone', '422.212',
 'The lowest commonly used saxophone. Its large size produces a deep, full sound fundamental to saxophone quartets, big bands, and contemporary orchestration.',
 'Western Europe', ARRAY['brass','metal keys'], 'Baritone_saxophone', now(), now()),

-- Brass
(gen_random_uuid(), 'French Horn', 'Cor', 'Aerophone', '423.232',
 'A coiled brass instrument with a conical bore and large bell, played with the right hand partially inserted into the bell. Orchestral horns typically play in pairs or groups of four. Known for their noble, warm tone.',
 'Western Europe', ARRAY['brass','nickel silver'], 'French_horn', now(), now()),

(gen_random_uuid(), 'Cornet', NULL, 'Aerophone', '423.233',
 'A valved brass instrument slightly smaller and more conical than the trumpet, giving it a mellower, rounder tone. Central to British brass bands and French orchestral music of the 19th century.',
 'Western Europe', ARRAY['brass'], 'Cornet_(instrument)', now(), now()),

(gen_random_uuid(), 'Flugelhorn', 'Flügelhorn', 'Aerophone', '423.233',
 'A wide-bore valved brass instrument closely related to the cornet. Has the warmest, darkest tone of the trumpet family. Used in brass bands, jazz, and occasionally orchestras.',
 'Western Europe', ARRAY['brass'], 'Flugelhorn', now(), now()),

(gen_random_uuid(), 'Tuba', NULL, 'Aerophone', '423.232',
 'The largest and lowest-pitched standard brass instrument. The harmonic foundation of the brass section. Uses valves to change pitch and requires exceptional lung capacity to play.',
 'Western Europe', ARRAY['brass'], 'Tuba', now(), now()),

(gen_random_uuid(), 'Euphonium', NULL, 'Aerophone', '423.232',
 'A medium-sized conical-bore brass instrument. Produces a mellow, rich baritone tone. Widely used in brass bands and wind ensembles, occasionally in orchestral works.',
 'Western Europe', ARRAY['brass'], 'Euphonium', now(), now()),

(gen_random_uuid(), 'Wagner Tuba', 'Wagnertuba', 'Aerophone', '423.232',
 'A hybrid instrument combining the mouthpiece of a horn with a tuba-like body. Created by Richard Wagner specifically for Der Ring des Nibelungen. Rare outside Wagnerian and Brucknerian repertoire.',
 'Western Europe', ARRAY['brass'], 'Wagner_tuba', now(), now()),

-- Percussion
(gen_random_uuid(), 'Timpani', 'Kettledrum', 'Membranophone', '211.11',
 'Large bowl-shaped drums with pedal-controlled tuning mechanisms. Always played in sets of two to four. The principal pitched percussion instrument of the orchestra — their thunderous rolls anchor the low end.',
 'Western Europe', ARRAY['copper','calfskin','mylar'], 'Timpani', now(), now()),

(gen_random_uuid(), 'Snare Drum', 'Caisse claire', 'Membranophone', '211.212.1',
 'A shallow double-headed drum with metal wire snares stretched across the lower head, producing the characteristic rattling buzz. Central to orchestral and military music.',
 'Western Europe', ARRAY['metal','wood','mylar'], 'Snare_drum', now(), now()),

(gen_random_uuid(), 'Bass Drum', 'Gran cassa', 'Membranophone', '211.212.1',
 'The largest drum in the orchestra, producing a deep, resonant boom when struck with a padded mallet. Provides dramatic impact and rhythmic punctuation.',
 'Western Europe', ARRAY['wood','mylar'], 'Bass_drum', now(), now()),

(gen_random_uuid(), 'Crash Cymbals', NULL, 'Idiophone', '111.142',
 'A pair of large brass plates that are struck together to produce a brilliant crash. One of the most powerful sounds in the orchestra, used for dramatic climaxes.',
 'Western Europe', ARRAY['brass alloy','bell metal'], 'Crash_cymbal', now(), now()),

(gen_random_uuid(), 'Suspended Cymbal', NULL, 'Idiophone', '111.142',
 'A single cymbal hung freely and struck with a stick or mallet. Produces a shimmering, sustained wash of sound used in orchestral and jazz music.',
 'Western Europe', ARRAY['brass alloy'], 'Cymbal', now(), now()),

(gen_random_uuid(), 'Glockenspiel', NULL, 'Idiophone', '111.212',
 'A percussion instrument consisting of tuned steel bars arranged like a piano keyboard and struck with mallets. Produces a bright, bell-like tone. Notably used in Mozart''s The Magic Flute.',
 'Western Europe', ARRAY['steel'], 'Glockenspiel', now(), now()),

(gen_random_uuid(), 'Xylophone', NULL, 'Idiophone', '111.212',
 'A pitched percussion instrument with wooden bars arranged like a keyboard, struck with hard mallets. Produces a dry, bright, percussive tone. Used in orchestral, folk, and contemporary music worldwide.',
 'Western Europe', ARRAY['rosewood','padouk'], 'Xylophone', now(), now()),

(gen_random_uuid(), 'Vibraphone', NULL, 'Idiophone', '111.212',
 'A metal-bar tuned percussion instrument with motor-driven rotating discs in the resonators that produce a characteristic vibrato. Central to jazz and 20th-century orchestral music.',
 'North America', ARRAY['aluminum bars','metal'], 'Vibraphone', now(), now()),

(gen_random_uuid(), 'Tubular Bells', 'Campane tubolari', 'Idiophone', '111.231',
 'Tuned metal tubes of varying length suspended vertically in a frame and struck with a mallet to simulate the sound of church bells. Used orchestrally for ceremonial and atmospheric effects.',
 'Western Europe', ARRAY['metal tubes'], 'Tubular_bells', now(), now()),

(gen_random_uuid(), 'Triangle', NULL, 'Idiophone', '111.211',
 'A small steel rod bent into a triangular shape, struck with a steel beater. Produces a high-pitched, clear, indefinitely sustaining ring. Despite its simplicity, it has important orchestral roles.',
 'Western Europe', ARRAY['steel'], 'Triangle_(musical_instrument)', now(), now()),

(gen_random_uuid(), 'Tam-tam', NULL, 'Idiophone', '111.241',
 'A large flat gong of East Asian origin used in the orchestra, struck with a soft mallet. Produces an enormous, slowly spreading wash of sound used for moments of great drama or mystery.',
 'East Asia', ARRAY['bronze'], 'Gong', now(), now()),

(gen_random_uuid(), 'Castanets', 'Castañuelas', 'Idiophone', '111.141',
 'A handheld percussion instrument from Spain consisting of two concave shells clacked together. Fundamental to Flamenco and Spanish orchestral music.',
 'Western Europe', ARRAY['hardwood','chestnut'], 'Castanets', now(), now()),

(gen_random_uuid(), 'Tambourine', NULL, 'Membranophone', '211.311',
 'A shallow single-headed frame drum with metal jingles set into its shell. Used in orchestral, folk, and popular music worldwide.',
 'Western Europe', ARRAY['wood','goatskin','metal jingles'], 'Tambourine', now(), now()),

-- Keyboards
(gen_random_uuid(), 'Harpsichord', 'Clavecin', 'Chordophone', '314.122',
 'A keyboard instrument in which strings are plucked by quills (plectra). Predecessor to the piano and the primary keyboard instrument of the Baroque era. Cannot vary volume by touch.',
 'Western Europe', ARRAY['spruce','walnut','brass quills'], 'Harpsichord', now(), now()),

(gen_random_uuid(), 'Pipe Organ', 'Orgue', 'Aerophone', '412.132',
 'The largest musical instrument, in which pressurized air is driven through pipes selected via a keyboard. Capable of an enormous range of timbres through its many stops (ranks of pipes).',
 'Western Europe', ARRAY['wood','metal pipes','leather'], 'Pipe_organ', now(), now()),

(gen_random_uuid(), 'Celesta', 'Céleste', 'Idiophone', '312.122-4',
 'A keyboard instrument in which hammers strike metal bars over wooden resonators. Produces a delicate, bell-like tone. Made famous by Tchaikovsky''s Dance of the Sugar Plum Fairy.',
 'Western Europe', ARRAY['steel bars','wood'], 'Celesta', now(), now()),

(gen_random_uuid(), 'Clavichord', NULL, 'Chordophone', '314.122',
 'The oldest and simplest keyboard string instrument, in which brass tangents strike strings. Produces a very soft tone but allows expressive dynamic nuance impossible on a harpsichord.',
 'Western Europe', ARRAY['spruce','brass'], 'Clavichord', now(), now()),

(gen_random_uuid(), 'Fortepiano', NULL, 'Chordophone', '314.122',
 'The early piano of the 18th and early 19th centuries, lighter in construction than the modern grand piano with a softer, more transparent sound. The instrument Mozart, Haydn, and early Beethoven composed for.',
 'Western Europe', ARRAY['spruce','leather hammers'], 'Fortepiano', now(), now()),

-- Plucked strings
(gen_random_uuid(), 'Classical Guitar', 'Guitarra clásica', 'Chordophone', '321.322',
 'A six-stringed acoustic instrument with nylon strings, played with fingernails or fingertips. The standard instrument for the solo guitar repertoire of the Baroque and Classical traditions.',
 'Western Europe', ARRAY['cedar','spruce','rosewood','nylon'], 'Classical_guitar', now(), now()),

(gen_random_uuid(), 'Lute', NULL, 'Chordophone', '321.321',
 'A plucked string instrument with a pear-shaped body and a distinctive angled pegbox. The primary chordal and solo instrument of European music from the Renaissance through the Baroque era.',
 'Western Europe', ARRAY['spruce','maple','ebony'], 'Lute', now(), now()),

(gen_random_uuid(), 'Theorbo', NULL, 'Chordophone', '321.321',
 'An extended bass lute with additional open bass strings (diapasons) on a second pegbox. Used in Baroque continuo playing to provide harmonic support.',
 'Western Europe', ARRAY['spruce','maple'], 'Theorbo', now(), now()),

(gen_random_uuid(), 'Mandolin', NULL, 'Chordophone', '321.322',
 'A short-necked lute with eight strings in four pairs (courses), played with a plectrum. Central to Italian classical music, bluegrass, and folk traditions across Europe and America.',
 'Western Europe', ARRAY['spruce','maple'], 'Mandolin', now(), now()),

(gen_random_uuid(), 'Banjo', NULL, 'Chordophone', '321.322',
 'A four or five-stringed instrument with a drum-like resonating chamber covered by a membrane head. Developed by African Americans, it is central to bluegrass, country, and Dixieland jazz.',
 'North America', ARRAY['wood','mylar','metal'], 'Banjo', now(), now()),

(gen_random_uuid(), 'Ukulele', NULL, 'Chordophone', '321.322',
 'A small four-stringed guitar-like instrument from Hawaii, originally adapted from the Portuguese machete. Associated with Hawaiian folk music and 20th-century popular music.',
 'Oceania', ARRAY['mahogany','spruce','nylon'], 'Ukulele', now(), now()),

-- Bowed strings
(gen_random_uuid(), 'Viola da gamba', 'Viol', 'Chordophone', '321.322',
 'A fretted bowed string instrument of the Renaissance and Baroque eras. Held between the legs, it has a lighter, more refined tone than the violin and was largely superseded by the cello.',
 'Western Europe', ARRAY['spruce','maple'], 'Viol', now(), now()),

(gen_random_uuid(), 'Hurdy-gurdy', 'Vielle à roue', 'Chordophone', '321.322',
 'A string instrument that produces sound by a hand-cranked rosined wheel rubbing against strings. Has a drone and melody strings and can be played continuously. Central to French and Eastern European folk music.',
 'Western Europe', ARRAY['maple','spruce'], 'Hurdy-gurdy', now(), now()),

-- Winds
(gen_random_uuid(), 'Recorder', 'Flauto dolce', 'Aerophone', '421.211.12',
 'An end-blown fipple flute family from Europe, ranging from garklein (tiny) to contrabass. The standard instrument of European art music before the transverse flute superseded it in the 18th century.',
 'Western Europe', ARRAY['boxwood','maple','plastic'], 'Recorder_(musical_instrument)', now(), now()),

(gen_random_uuid(), 'Bagpipes', NULL, 'Aerophone', '422.112',
 'A wind instrument using enclosed reeds fed from a constant reservoir of air in a bag. Found across Europe, North Africa, and parts of Asia in many regional variants (Highland, Galician, Northumbrian, etc.).',
 'Western Europe', ARRAY['goatskin','wood','metal'], 'Bagpipes', now(), now()),

(gen_random_uuid(), 'Accordion', NULL, 'Aerophone', '412.132',
 'A free-reed bellows instrument with a piano or button keyboard. Developed in early 19th-century Europe and widely adopted in folk music across Europe, Latin America, and beyond.',
 'Western Europe', ARRAY['metal reeds','wood','leather bellows'], 'Accordion', now(), now()),

(gen_random_uuid(), 'Concertina', NULL, 'Aerophone', '412.132',
 'A small hexagonal free-reed bellows instrument. Central to English and Anglo folk music, Irish traditional music, and South American tango (as the bandoneón variant).',
 'Western Europe', ARRAY['metal reeds','wood'], 'Concertina', now(), now()),

(gen_random_uuid(), 'Harmonica', NULL, 'Aerophone', '412.132',
 'A small free-reed wind instrument played by blowing and drawing air through chambers. Central to blues, country, folk, and rock music. Also called the mouth organ.',
 'Western Europe', ARRAY['metal reeds','wood','metal'], 'Harmonica', now(), now())

ON CONFLICT (name) DO UPDATE SET
  hs_category      = COALESCE(EXCLUDED.hs_category, instruments.hs_category),
  hornbostel_sachs = COALESCE(EXCLUDED.hornbostel_sachs, instruments.hornbostel_sachs),
  description      = EXCLUDED.description,
  origin_region    = COALESCE(EXCLUDED.origin_region, instruments.origin_region),
  materials        = COALESCE(EXCLUDED.materials, instruments.materials),
  wikipedia_slug   = COALESCE(EXCLUDED.wikipedia_slug, instruments.wikipedia_slug),
  updated_at       = now();
