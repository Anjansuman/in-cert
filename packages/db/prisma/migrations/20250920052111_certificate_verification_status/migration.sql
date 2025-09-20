-- AlterTable
ALTER TABLE "public"."Certificate" ADD COLUMN     "verification" "public"."VerificationStatus" NOT NULL DEFAULT 'VERIFIED';
