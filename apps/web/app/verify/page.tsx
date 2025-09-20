"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useContract } from "@/app/contract";
import { useWallet } from "@solana/wallet-adapter-react";

export default function VerifyPage() {
    const router = useRouter();

    const [refFile, setRefFile] = useState<File | null>(null);
    const [testFile, setTestFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<null | {
        reference: string;
        tested: string;
        status: string;
        analysisReport?: string;
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
        setResult(null);

        try {
            const formData = new FormData();
            formData.append("test_file", testFile);
            formData.append("reference_file", refFile);

            const response = await fetch("http://127.0.0.1:8000/analyze", {
                method: "POST",
                body: formData,
            });

            const reportText = await response.text();

            if (response.ok) {
                setResult({
                    reference: refFile.name,
                    tested: testFile.name,
                    status: "Verified Successfully",
                    analysisReport: reportText,
                });
            } else {
                setResult({
                    reference: refFile.name,
                    tested: testFile.name,
                    status: "Verification Failed",
                    analysisReport: reportText,
                });
            }

        } catch (err: any) {
            console.error("Verification Error:", err);
            setResult({
                reference: refFile.name,
                tested: testFile.name,
                status: "Error connecting to backend",
                analysisReport: err.message,
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
                    {/* Reference Certificate */}
                    <div>
                        <label className="block mb-2 font-medium">📑 Reference Certificate</label>
                        <input
                            type="file"
                            accept="application/pdf"
                            onChange={handleRefFile}
                            className="w-full p-2 rounded-lg bg-zinc-900 border border-zinc-700 text-white"
                        />
                        {refFile && (
                            <iframe
                                src={URL.createObjectURL(refFile)}
                                className="w-full h-48 mt-3 rounded-md border border-zinc-700"
                            />
                        )}
                    </div>

                    {/* Test Certificate */}
                    <div>
                        <label className="block mb-2 font-medium">📄 Test Certificate</label>
                        <input
                            type="file"
                            accept="application/pdf"
                            onChange={handleTestFile}
                            className="w-full p-2 rounded-lg bg-zinc-900 border border-zinc-700 text-white"
                        />
                        {testFile && (
                            <iframe
                                src={URL.createObjectURL(testFile)}
                                className="w-full h-48 mt-3 rounded-md border border-zinc-700"
                            />
                        )}
                    </div>

                    {/* Verify Button */}
                    <button
                        onClick={verifyCertificates}
                        disabled={loading}
                        className={`w-full py-2 rounded-lg font-medium shadow-md transition ${
                            loading
                                ? "bg-gray-600 cursor-not-allowed"
                                : "bg-green-500 hover:bg-green-400 text-black"
                        }`}
                    >
                        {loading ? "Verifying..." : "Verify Certificate"}
                    </button>

                    {/* Results */}
                    {result && (
                        <div className="bg-zinc-900 border border-zinc-700 p-4 rounded-lg mt-4">
                            <h2 className="font-semibold text-lg mb-2">Result & Analysis</h2>
                            <p className="mb-2">
                                <strong>Reference:</strong> {result.reference}<br />
                                <strong>Tested:</strong> {result.tested}<br />
                                <strong>Status:</strong> {result.status}
                            </p>
                            {result.analysisReport && (
                                <pre className="whitespace-pre-wrap text-sm bg-zinc-800 p-3 rounded-md text-white overflow-x-auto">
                                    {result.analysisReport}
                                </pre>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </section>
    );
}
