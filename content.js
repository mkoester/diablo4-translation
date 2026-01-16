// D4 Glyph Translator - Translates German glyph names to English
// Format: "German (English)"

const translations = {
  "Macht": "Might",
  "Zorn": "Wrath",
  "Zermalmer": "Crusher",
  "Poltern": "Rumble",
  "Unerschrocken": "Undaunted",
  "Rache": "Revenge",
  "Marschall": "Marshal",
  "Groll": "Ire",
  "Brodelnd": "Seething",
  "Tornado": "Twister",
  "Beidhändig": "Ambidextrous",
  "Blutfresser": "Bloodfeeder",
  "Rauferei": "Brawl",
  "Reißer und Klaue": "Fang and Claw",
  "Geist": "Spirit",
  "Hüter": "Keeper",
  "Werbär": "Werebear",
  "Werwolf": "Werewolf",
  "Gestaltwandler": "Shapeshifter",
  "Schützer": "Protector",
  "Kontrolle": "Control",
  "Dominieren": "Dominate",
  "Essenz": "Essence",
  "Grabhüter": "Gravekeeper",
  "Totenbeleber": "Deadraiser",
  "Schändung": "Desecration",
  "Golem": "Golem",
  "Abyssal": "Abyssal",
  "Dunkelheit": "Darkness",
  "Verstärken": "Amplify",
  "Entladen": "Fulminate",
  "Entfesseln": "Unleash",
  "Aufgeladen": "Charged",
  "Zertrümmerung": "Destruction",
  "Zerstörung": "Destruction",
  "Winter": "Winter",
  "Abschirmend": "Warding",
  "Elementarist": "Elementalist",
  "Kopfjäger": "Headhunter",
  "Ausbeuten": "Exploit",
  "Übertreffen": "Outmatch",
  "Kolossal": "Colossal",
  "Verfolger": "Tracker",
  "Lauffeuer": "Wildfire",
  "Vielseitigkeit": "Versatility",
  "Splitter": "Chip",
  "Absorbierer": "Imbiber",
  "Schlinger": "Guzzler",
  "Hybris": "Hubris",
  "Hinterhalt": "Ambush",
  "Verringern": "Diminish",
  "Fluidität": "Fluidity",
  "Tödliche Flinkheit": "Fluidity",
  "Falle": "Snare",
  "Nähe": "Snare",
  "Verschlagen": "Devious",
  "Herausforderer": "Challenger",
  "Körperlich": "Corporeal",
  "Auslöscher": "Eliminator",
  "Eitern": "Fester",
  "Besonnen": "Canny",
  "Anrufung": "Invocation",
  "Klaue": "Talon",
  "Stolz": "Turf",
  "Gezackte Feder": "Jagged Plume",
  "Menagerist": "Menagerist",
  "Kryopathie": "Cryopathy",
  "Frostfresser": "Frostfeeder",
  "Pyromane": "Pyromaniac",
  "Explosiv": "Explosive",
  "Magier": "Mage",
  "Wächter": "Sentinel",
  "Taktiker": "Tactician",
  "Inbrünstig": "Feverous",
  "Pracht": "Resplendence",
  "Geschliffen": "Honed",
  "Apostel": "Apostle",
  "Richter": "Judicator",
  "Schleifen": "Hone",
  "Gebieter": "Arbiter",
  "Gesetz": "Law",
  "Beschörer": "Conjurer",
  "Beschwörer": "Conjurer",
  "Ritual": "Ritual",
  "Angeboren": "Innate",
  "Gebiet": "Territorial",
  "Territorial": "Territorial",
  "Flammenfresser": "Flamefeeder",
  "Elektroschock": "Electrocution",
  "Stromschlag": "Electrocute",
  "Tektonisch": "Tectonic",
  "Effizienz": "Efficacy",
  "Adept": "Adept",
  "Aufopferung": "Sacrificial",
  "Waffenmeister": "Weapon Master",
  "Kampf": "Combat",
  "Verstärkt": "Reinforced",
  "Spalter": "Cleaver",
  "Krieger": "Warrior",
  "Geißel": "Scourge",
  "Verzauberer": "Enchanter",
  "Nachtpirscher": "Nightstalker",
  "Fackel": "Torch",
  "Henker": "Executioner",
  "Haltung": "Poise",
  "Wildnis": "Wilds",
  "Waldläufer": "Ranger",
  "Exhumierung": "Exhumation",
  "Konsum": "Consumption",
  "Wandler": "Shifter",
  "Erde und Himmel": "Earth and Sky",
  "Mensch": "Human",
  "Fluch": "Bane",
  "Näher": "Closer",
  "Bluttrinker": "Blood-drinker"
};

// Sort by length (longest first) to avoid partial replacements
const sortedKeys = Object.keys(translations).sort((a, b) => b.length - a.length);

// Build regex pattern for all German terms
const pattern = new RegExp(
  '\\b(' + sortedKeys.map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')\\b',
  'g'
);

// Track processed nodes to avoid double-processing
const processedNodes = new WeakSet();

function translateTextNode(textNode) {
  if (processedNodes.has(textNode)) return;

  const originalText = textNode.textContent;
  let newText = originalText;

  // Replace each German term with "German (English)" format
  newText = newText.replace(pattern, (match) => {
    const english = translations[match];
    if (english && !originalText.includes(`(${english})`)) {
      return `${match} (${english})`;
    }
    return match;
  });

  if (newText !== originalText) {
    textNode.textContent = newText;
    processedNodes.add(textNode);
  }
}

function walkTextNodes(element) {
  const walker = document.createTreeWalker(
    element,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: (node) => {
        // Skip script, style, and already processed nodes
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        const tagName = parent.tagName.toLowerCase();
        if (tagName === 'script' || tagName === 'style' || tagName === 'noscript') {
          return NodeFilter.FILTER_REJECT;
        }
        // Only process nodes with actual text content
        if (node.textContent.trim().length === 0) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    }
  );

  const textNodes = [];
  while (walker.nextNode()) {
    textNodes.push(walker.currentNode);
  }

  textNodes.forEach(translateTextNode);
}

// Initial translation pass - only within paragon board rows
function initialTranslation() {
  document.querySelectorAll('.d4para-row').forEach(row => {
    walkTextNodes(row);
  });
}

// Observe DOM for dynamic content
function setupObserver() {
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      // Handle added nodes - only within .d4para-row elements
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === Node.ELEMENT_NODE) {
          if (node.classList?.contains('d4para-row')) {
            walkTextNodes(node);
          } else if (node.closest('.d4para-row')) {
            walkTextNodes(node);
          } else if (node.querySelectorAll) {
            node.querySelectorAll('.d4para-row').forEach(row => walkTextNodes(row));
          }
        } else if (node.nodeType === Node.TEXT_NODE) {
          if (node.parentElement?.closest('.d4para-row')) {
            translateTextNode(node);
          }
        }
      });

      // Handle character data changes - only within .d4para-row elements
      if (mutation.type === 'characterData' && mutation.target.nodeType === Node.TEXT_NODE) {
        if (mutation.target.parentElement?.closest('.d4para-row')) {
          processedNodes.delete(mutation.target);
          translateTextNode(mutation.target);
        }
      }
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true,
    characterData: true
  });
}

// Run when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    initialTranslation();
    setupObserver();
  });
} else {
  initialTranslation();
  setupObserver();
}

console.log('D4 Glyph Translator loaded - translating German glyph names to English');
