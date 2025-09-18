import ContractClass from "@/src/contract/ContractClass";
import { useConnection, useWallet } from "@solana/wallet-adapter-react";
import React, { createContext, useContext, useEffect, useState } from "react";

type ContractContextType = {
    contract: ContractClass | null;
}

const ContractContext = createContext<ContractContextType>({
    contract: null,
});

export const ContractProvider = ({ children }: { children: React.ReactNode }) => {
    const { connection } = useConnection();
    const wallet = useWallet();
    const [contract, setContract] = useState<ContractClass | null>(null);

    useEffect(() => {
        if (wallet.connected && wallet.publicKey) {
            try {

                const contractInstance = new ContractClass(connection, wallet);
                setContract(contractInstance);

            } catch (error) {
                console.error("Contract initialization failed: ", error);
            }
        } else {
            setContract(null);
        }
    }, [wallet.connected, wallet.publicKey, connection]);

    return (
        <ContractContext.Provider value={{ contract }}>
            {children}
        </ContractContext.Provider>
    );
}

export const useContract = () => useContext(ContractContext);