interface AuthInstitute {
    institutionId: String,
    institutionName: String,
}

declare namespace Express {
    export interface Request {
        institution?: AuthInstitute
    }
}