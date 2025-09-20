import { Address, AnchorProvider, BN, Idl, Program } from "@coral-xyz/anchor";

import { WalletContextState } from "@solana/wallet-adapter-react";
import { Connection, PublicKey, SystemProgram } from "@solana/web3.js";

import { Contract } from "./contract";
import idl from "./contract.json";

export default class ContractClass {

    private program: Program<Contract> | null = null;
    private provider: AnchorProvider | null = null;
    private wallet: WalletContextState | null = null;

    constructor(connection: Connection, wallet: WalletContextState) {
        if (!wallet.publicKey || !wallet.signTransaction) throw new Error('Wallet not connected or incomplete!');

        this.init(connection, wallet);
    }

    private init(connection: Connection, wallet: WalletContextState) {
        try {

            this.wallet = wallet;

            this.provider = new AnchorProvider(
                connection,
                wallet as any,
                {
                    commitment: 'confirmed',
                },
            );

            this.program = new Program<Contract>(idl as Idl, this.provider);

        } catch (error) {
            this.handleError(error);
        }
    }

    public async createCertificate(
        institutionId: string,
        institutionName: string,
        candidateId: string,
        candidateName: string,
        issuedAt: number,
        description: string,
        uri?: string | null,
    ): Promise<string | null> {
        try {

            if (!this.program) throw new Error('Program not initialized!');

            console.log("InstitutionId bytes:", Buffer.from(institutionId));
            console.log("CandidateId bytes:", Buffer.from(candidateId));
            console.log("IssuedAt seconds:", issuedAt);

            const [certificatePDA] = this.getCertificatePda(institutionId, candidateId);

            console.log({ certificatePDA });

            const res = await this.program.methods
                .createCertificate(
                    institutionId,
                    candidateId,
                    institutionName,
                    candidateName,
                    new BN(issuedAt),
                    description,
                    uri || null,
                )
                .accountsStrict({
                    certificate: certificatePDA,
                    authority: this.getWalletPublicKey(),
                    systemProgram: SystemProgram.programId,
                })
                .signers([])
                .rpc();

            return res;

        } catch (error) {
            this.handleError(error);
            return null;
        }
    }

    public async getCertificate(address: Address): Promise<any> {
        try {

            if (!this.program) throw new Error('Program not initialized!');

            const certificate = await this.program.account.certificate.fetch(address);

            return certificate;

        } catch (error) {
            this.handleError(error);
            return null;
        }
    }

    public async getAllCertificate(): Promise<any[]> {
        try {

            if(!this.program) throw new Error('Program not initialized!');

            const certificates = await this.program.account.certificate.all();

            console.log({ certificates });

            return certificates;
            
        } catch (error) {
            this.handleError(error);
            return [];
        }
    }

    private getCertificatePda(institutionId: String, candidateId: String): [PublicKey, number] {
        if (!this.program) throw new Error('Program not initialized!');

        return PublicKey.findProgramAddressSync(
            [
                Buffer.from('certificate'),
                Buffer.from(institutionId),
                Buffer.from(candidateId),
            ],
            this.program.programId,
        );
    }

    public getWalletPublicKey(): PublicKey {
        if (!this.wallet?.publicKey) throw new Error('Wallet not connected');

        return this.wallet.publicKey;
    }

    private handleError(error: unknown): void {
        console.error('Contract error: ', error);

        if (typeof error === 'string') {
            throw new Error(error);
        } else if (error instanceof Error) {
            throw error;
        }
        throw new Error('Unknown contract error!');
    }

}