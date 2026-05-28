export interface BasicOption {
  id: string;
  name: string;
}

export interface QuoteOptions {
  property_types: BasicOption[];
  work_locations: BasicOption[];
  service_types: BasicOption[];
  paints: BasicOption[];
  color_intensities: BasicOption[];
  surface_states: BasicOption[];
  textures: BasicOption[];
  advance_difficulties: BasicOption[];
  occupancies: BasicOption[];
  height_risks: BasicOption[];
  area_protections: BasicOption[];
  preparations: BasicOption[];
  schedules: BasicOption[];
  states: BasicOption[];
}

export interface QuoteForm {
  property_type: string;
  work_location: string;
  square_meters: string;

  service_type: string;
  paint_product: string;
  color_intensity: string;

  surface_state: string;
  texture: string;
  advance_difficulty: string;
  occupancy: string;
  height_risk: string;
  area_protection: string;
  preparation: string[];
  schedule: string;
  place_activities: string;

  state: string;
  city: string;
  postal_code: string;

  customer_name: string;
  contact_method: string;
  contact_value: string;
  wants_offers: boolean;
}

export interface QuotePayload extends Omit<QuoteForm, "square_meters"> {
  square_meters: number;
}

export interface QuoteAdjustment {
  category: string;
  option_id: string;
  option_name: string;
  percentage: number;
  amount: number;
}

export interface QuoteResult {
  customer_name: string;
  paint_product: string;
  paint_product_name: string;
  base_price_per_m2: number;
  total_adjustment_percentage: number;
  adjusted_price_per_m2: number;
  square_meters: number;
  subtotal: number;
  adjustments: QuoteAdjustment[];
  estimated_price: number;
}
