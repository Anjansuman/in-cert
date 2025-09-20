// components/PDFCertificate.tsx
"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import QRCodeLib from "qrcode";
import { PDFDownloadLink, Document, Page, View, Text, Image, StyleSheet } from "@react-pdf/renderer";

type CertificateProps = {
    id: string;
};

export default function PDFCertificate({ id }: CertificateProps) {
    const [certificateData, setCertificateData] = useState<any>();
    const [qrDataUrl, setQrDataUrl] = useState<string | null>(null);

    useEffect(() => {
        async function fetchData() {
            if (!id) return;
            const { data } = await axios.get(`http://localhost:8080/api/v1/get-certificate/${id}`);
            setCertificateData(data.certificate);

            // Generate QR code for JWT
            const qrUrl = await QRCodeLib.toDataURL(data.certificate.jwt, {
                errorCorrectionLevel: "H",
                color: { dark: "#000000", light: "#ffffff" },
            });
            setQrDataUrl(qrUrl);
        }

        fetchData();
    }, [id]);

    if (!certificateData) return <p>Loading Certificate...</p>;

    const explorerUrl = `https://explorer.solana.com/tx/${certificateData.nftHash}?cluster=devnet`;

    // PDF styles
    const styles = StyleSheet.create({
        page: {
            backgroundColor: "#f3f4f6",
            padding: 40,
            fontFamily: "Helvetica",
            color: "#1f2937",
        },
        header: {
            textAlign: "center",
            marginBottom: 20,
        },
        title: {
            fontSize: 32,
            fontWeight: "bold",
            color: "#064e3b",
            letterSpacing: 2,
        },
        subtitle: {
            fontSize: 18,
            color: "#4b5563",
            marginTop: 5,
        },
        candidate: {
            textAlign: "center",
            marginVertical: 20,
        },
        candidateName: {
            fontSize: 28,
            fontWeight: "bold",
            textDecoration: "underline",
            textDecorationColor: "#065f46",
            color: "#111827",
            marginTop: 10,
        },
        description: {
            fontSize: 16,
            color: "#4b5563",
            marginTop: 10,
            maxWidth: "80%",
            alignSelf: "center",
        },
        footer: {
            flexDirection: "row",
            justifyContent: "space-between",
            marginTop: 30,
            alignItems: "flex-end",
        },
        qrImage: {
            width: 120,
            height: 120,
            backgroundColor: "#d1d5db",
            padding: 2,
            borderRadius: 4,
        },
        infoText: {
            fontSize: 12,
            color: "#4b5563",
        },
        highlight: {
            color: "#111827",
        },
        verification: {
            fontSize: 12,
            fontWeight: "bold",
        },
        nftHash: {
            fontSize: 10,
            marginTop: 4,
        },
    });

    const CertificateDocument = (
        <Document>
            <Page size="A4" style={styles.page}>
                {/* Header */}
                <View style={styles.header}>
                    <Text style={styles.title}>Certificate of Achievement</Text>
                    <Text style={styles.subtitle}>
                        Awarded by {certificateData.institution.name}
                    </Text>
                </View>

                {/* Candidate Info */}
                <View style={styles.candidate}>
                    <Text style={styles.subtitle}>This is to certify that</Text>
                    <Text style={styles.candidateName}>{certificateData.candidateName}</Text>
                    <Text style={styles.description}>{certificateData.description}</Text>
                </View>

                {/* Footer */}
                <View style={styles.footer}>
                    {/* Left */}
                    <View>
                        {qrDataUrl && <Image style={styles.qrImage} src={qrDataUrl} />}
                        <Text style={styles.infoText}>
                            Issued At: <Text style={styles.highlight}>{new Date(certificateData.issuedAt).toDateString()}</Text>
                        </Text>
                        <Text style={styles.infoText}>
                            Certificate ID: <Text style={styles.highlight}>{certificateData.id}</Text>
                        </Text>
                    </View>

                    {/* Right */}
                    <View>
                        <Text style={[styles.infoText, styles.verification]}>
                            Verification Status:{" "}
                            <Text
                                style={{
                                    color: certificateData.verification === "VERIFIED" ? "#22c55e" : "#ef4444",
                                }}
                            >
                                {certificateData.verification}
                            </Text>
                        </Text>
                        <Text style={styles.nftHash}>NFT Hash: {certificateData.nftHash}</Text>
                        <Text style={[styles.nftHash, { color: "#3b82f6" }]}>
                            View on Solana Explorer: {explorerUrl}
                        </Text>
                    </View>
                </View>
            </Page>
        </Document>
    );

    return (
        <div className="flex flex-col items-center gap-4">
            <PDFDownloadLink
                document={CertificateDocument}
                fileName={`certificate-${certificateData.candidateName}.pdf`}
                style={{
                    padding: "10px 20px",
                    backgroundColor: "#0f766e",
                    color: "#ffffff",
                    borderRadius: 6,
                    textDecoration: "none",
                    fontWeight: "bold",
                }}
            >
                Download Certificate PDF
            </PDFDownloadLink>
        </div>
    );
}
