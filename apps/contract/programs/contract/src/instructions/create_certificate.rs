use anchor_lang::prelude::*;

use crate::state::certificate::Certificate;

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

    let certificate = &mut ctx.accounts.certificate;

    certificate.institution = ctx.accounts.authority.key();
    certificate.institution_id = institution_id;
    certificate.institution_name = institution_name;
    certificate.candidate_id = candidate_id;
    certificate.candidate_name = candidate_name;
    certificate.issued_at = issued_at;
    certificate.description = description;
    certificate.uri = uri;

    Ok(())
}

#[derive(Accounts)]
#[instruction(institution_id: String, candidate_id: String, issued_at: i64)]
pub struct CreateCertificate<'info> {
    #[account(
        init,
        seeds = [
            b"certificate",
            institution_id.as_bytes(),
            candidate_id.as_bytes(),
            &issued_at.to_le_bytes(),
        ],
        bump,
        payer = authority,
        space = 8 + Certificate::len(),
    )]
    pub certificate: Account<'info, Certificate>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}
