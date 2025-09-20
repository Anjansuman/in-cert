"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
    const router = useRouter();
    const [signInOpen, setSignInOpen] = useState(false);

    return (
        <div className="dark font-poppins text-gray-200 bg-gradient-to-br from-gray-500 via-gray-900 to-black min-h-screen">


            {signInOpen && (
                <div className="fixed inset-0 bg-black/70 flex justify-center items-center z-50">
                    <div className="bg-gray-900 p-8 rounded-2xl w-80 text-center shadow-lg">
                        <h2 className="text-2xl mb-4">Sign In</h2>
                        <input
                            type="text"
                            placeholder="Username"
                            className="w-full p-2 mb-3 rounded-md bg-gray-800 text-gray-200"
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            className="w-full p-2 mb-3 rounded-md bg-gray-800 text-gray-200"
                        />
                        <button
                            onClick={() => {
                                alert("Signed in successfully!");
                                setSignInOpen(false);
                            }}
                            className="w-full bg-green-400 text-black font-bold py-2 rounded-md hover:bg-green-500 transition"
                        >
                            Sign In
                        </button>
                        <button
                            onClick={() => setSignInOpen(false)}
                            className="w-full mt-2 bg-red-500 py-2 rounded-md hover:bg-red-600 transition"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            )}

            <main className="pt-32 px-6 md:px-20">
                <section className="text-center">
                    <h1 className="text-4xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-yellow-400 mb-3">
                        Welcome to In-Cert
                    </h1>
                    <h2 className="text-xl italic text-gray-300 mb-3">
                        “In-Cert — Verify Fast. Certify Smart.”
                    </h2>
                    <p className="text-gray-400 mb-10 max-w-xl mx-auto">
                        Manage, verify, and create certificates securely and effortlessly,
                        all in one platform.
                    </p>

                    <div className="flex flex-wrap justify-center gap-10">
                        <div className="bg-gray-800/70 backdrop-blur-md border border-white/10 p-8 rounded-2xl w-72 hover:scale-105 transition shadow-lg">
                            <h2 className="text-2xl font-semibold mb-3">Upload Certificate</h2>
                            <p className="text-gray-300 mb-5">
                                Upload and verify your certificate securely.
                            </p>
                            <button
                                onClick={() => router.push("/verify")}
                                className="w-full py-2 rounded-lg bg-cyan-400 text-black font-medium hover:bg-cyan-500 hover:scale-105 transition"
                            >
                                Verify Certificate
                            </button>
                        </div>

                        <div className="bg-gray-800/70 backdrop-blur-md border border-white/10 p-6 rounded-2xl w-72 hover:scale-105 transition shadow-lg">
                            <h2 className="text-2xl font-semibold mb-3">
                                Generate Certificate
                            </h2>
                            <p className="text-gray-300 mb-5">
                                Create and customize professional certificates.
                            </p>
                            <button
                                onClick={() => router.push("/create")}
                                className="w-full py-2 rounded-lg bg-yellow-400 text-black font-medium hover:bg-yellow-500 hover:scale-105 transition"
                            >
                                Generate Certificate
                            </button>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
}
