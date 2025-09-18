import CertificateInput from "@/src/components/app/Certificate/CertificateInput";
import Navbar from "@/src/components/app/Navbar/Navbar";
import Image from "next/image";

export default function Home() {
    return (
        <div className="h-screen bg-neutral-900 ">
            <Navbar />
            <div className="h-full w-full flex justify-center items-center">
                <CertificateInput />
            </div>
        </div>
    );
}
