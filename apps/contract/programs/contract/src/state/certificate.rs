use anchor_lang::prelude::*;

#[account]
pub struct Certificate {
    pub institution: Pubkey,
    pub institution_id: String,
    pub institution_name: String,
    pub candidate_id: String,
    pub candidate_name: String,
    pub issued_at: i64,
    pub description: String,
    pub uri: Option<String>,
}

impl Certificate {
    pub fn len() -> usize {
        32 +        // institution pubkey
        4 + 32 +    // institution_id (max 32 chars)
        4 + 64 +    // institution_name (max 64 chars)
        4 + 32 +    // candidate_id (max 32 chars)
        4 + 64 +    // candidate_name (max 64 chars)
        8 +         // issued_at (i64)
        4 + 128 +   // description (max 128 chars)
        1 + 4 + 200 // Option<String> uri (1 byte for Option, 4 + len for string; allow 200 chars)
    }
}
