// Symptoms catalogue — preserving all original ids, names and icons.
// Added: category field for filter tabs. emergency flag for safety warnings.

const symptomsData = [
  { id: 1,  name: 'Fever',               icon: 'Thermometer',    category: 'General'     },
  { id: 2,  name: 'Headache',            icon: 'Brain',          category: 'Pain'        },
  { id: 3,  name: 'Cough',               icon: 'Wind',           category: 'Respiratory' },
  { id: 4,  name: 'Fatigue',             icon: 'BatteryLow',     category: 'General'     },
  { id: 5,  name: 'Nausea',              icon: 'Frown',          category: 'Digestive'   },
  { id: 6,  name: 'Vomiting',            icon: 'Droplets',       category: 'Digestive'   },
  { id: 7,  name: 'Dizziness',           icon: 'RotateCcw',      category: 'Other'       },
  { id: 8,  name: 'Chest Pain',          icon: 'HeartPulse',     category: 'Pain',        emergency: true },
  { id: 9,  name: 'Stomach Pain',        icon: 'AlertCircle',    category: 'Digestive'   },
  { id: 10, name: 'Joint Pain',          icon: 'Anchor',         category: 'Pain'        },
  { id: 11, name: 'Skin Rash',           icon: 'Fingerprint',    category: 'Skin'        },
  { id: 12, name: 'Weakness',            icon: 'TrendingDown',   category: 'General'     },
  { id: 13, name: 'Chills',              icon: 'Snowflake',      category: 'General'     },
  { id: 14, name: 'Sore Throat',         icon: 'Mic',            category: 'Respiratory' },
  { id: 15, name: 'Runny Nose',          icon: 'Droplet',        category: 'Respiratory' },
  { id: 16, name: 'Shortness of Breath', icon: 'CloudDrizzle',   category: 'Respiratory', emergency: true },
  { id: 17, name: 'Back Pain',           icon: 'ArrowDownUp',    category: 'Pain'        },
  { id: 18, name: 'Muscle Pain',         icon: 'Zap',            category: 'Pain'        },
  { id: 19, name: 'Sweating',            icon: 'Waves',          category: 'General'     },
  { id: 20, name: 'Loss of Appetite',    icon: 'UtensilsCrossed', category: 'General'    },
  { id: 21, name: 'Blurred Vision',      icon: 'Eye',            category: 'Other'       },
  { id: 22, name: 'Swelling',            icon: 'Maximize',       category: 'Skin'        },
  { id: 23, name: 'Insomnia',            icon: 'Moon',           category: 'General'     },
  { id: 24, name: 'Anxiety',             icon: 'AlertTriangle',  category: 'Other'       },
];

export default symptomsData;
