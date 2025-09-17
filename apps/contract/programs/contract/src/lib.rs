pub mod instructions;
pub mod state;


use anchor_lang::prelude::*;
use instructions::*;



declare_id!("9nF17epkj1esEvgx4JpkviUfn2XbEheBDUsiuqAt6ogc");

#[program]
pub mod contract {

    use super::*;

    // and here also add verified institution check
    pub fn create_certificate(
        ctx: Context<CreateCertificate>,
        institution_id: String,
        institution_name: String,
        candidate_id: String,
        candidate_name: String,
        issued_at: i64,
        description: String,
        uri: Option<String>,
    ) -> Result<()> {
        instructions::create_certificate::create_certificate(
            ctx,
            institution_id,
            institution_name,
            candidate_id,
            candidate_name,
            issued_at,
            description,
            uri,
        )
    }

    // a fn for adding institution in chain for govt verified bodies, and checking everytime for security
    
}