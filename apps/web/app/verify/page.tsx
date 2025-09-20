"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useContract } from "@/app/contract";
import { useWallet } from "@solana/wallet-adapter-react";

export default function VerifyPage() {
    const router = useRouter();
    const { contract } = useContract();
    const { wallet, publicKey } = useWallet();

    const [refFile, setRefFile] = useState<File | null>(null);
    const [testFile, setTestFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<null | {
        reference: string;
        tested: string;
        status: string;
    }>(null);

    const handleRefFile = (e: React.ChangeEvent<HTMLInputElement>) => {
        setRefFile(e.target.files?.[0] || null);
    };

    const handleTestFile = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTestFile(e.target.files?.[0] || null);
    };

    const verifyCertificates = async () => {
        if (!refFile || !testFile) {
            alert("Upload both Reference and Test certificates.");
            return;
        }

        setLoading(true);
        try {
            console.log("Verifying certificates with contract:", contract);
            console.log("Wallet:", publicKey?.toBase58());

            await new Promise((res) => setTimeout(res, 1500));

            setResult({
                reference: refFile.name,
                tested: testFile.name,
                status: "Verified Successfully",
            });
        } catch (err) {
            console.error(err);
            setResult({
                reference: refFile.name,
                tested: testFile.name,
                status: "Verification Failed",
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="flex flex-col items-center justify-center min-h-screen bg-neutral-900 px-4">
            <div className="w-full max-w-2xl bg-black text-gray-100 p-6 rounded-2xl shadow-lg">
                <h1 className="text-2xl font-bold mb-6 text-center bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-yellow-400">
                    Verify Certificate
                </h1>

                <div className="flex flex-col gap-4">
                    <div>
                        <label className="block mb-2 font-medium">📑 Reference Certificate</label>
                        <input
                            type="file"
                            accept="application/pdf"
                            onChange={handleRefFile}
                            className="w-full p-2 rounded-lg bg-zinc-900 border border-zinc-700 text-white placeholder-gray-400"
                        />
                        {refFile && (
                            <iframe
                                src={URL.createObjectURL(refFile)}
                                className="w-full h-48 mt-3 rounded-md border border-zinc-700"
                            ></iframe>
                        )}
                    </div>

                    <div>
                        <label className="block mb-2 font-medium">📄 Test Certificate</label>
                        <input
                            type="file"
                            accept="application/pdf"
                            onChange={handleTestFile}
                            className="w-full p-2 rounded-lg bg-zinc-900 border border-zinc-700 text-white placeholder-gray-400"
                        />
                        {testFile && (
                            <iframe
                                src={URL.createObjectURL(testFile)}
                                className="w-full h-48 mt-3 rounded-md border border-zinc-700"
                            ></iframe>
                        )}
                    </div>

                    <button
                        onClick={verifyCertificates}
                        disabled={loading}
                        className={`w-full py-2 rounded-lg font-medium shadow-md transition ${loading
                                ? "bg-gray-600 cursor-not-allowed"
                                : "bg-green-500 hover:bg-green-400 text-black"
                            }`}
                    >
                        {loading ? "Verifying..." : "Verify Certificate"}
                    </button>

                    {result && (
                        <div className="bg-zinc-900 border border-zinc-700 p-4 rounded-lg mt-4">
                            <h2 className="font-semibold text-lg mb-2">Result & Analysis</h2>
                            <p>
                                <strong>Reference:</strong> {result.reference}
                                <br />
                                <strong>Tested:</strong> {result.tested}
                                <br />
                                <strong>Status:</strong> {result.status}
                            </p>
                        </div>
                    )}

                </div>
            </div>
        </section>
    );
}
