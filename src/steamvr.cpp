#include "CSteamworks.h"
#include "steamvr.h"

vr::IHmd *s_Hmd;
vr::IHmd *Hmd() {
	return s_Hmd;
}

SB_API vr::IHmd *S_CALLTYPE VR_Init_(vr::HmdError *peError) {
	s_Hmd = vr::VR_Init(peError);
	return s_Hmd;
}

SB_API void S_CALLTYPE VR_Shutdown_() {
	s_Hmd = NULL;
	return vr::VR_Shutdown();
}

SB_API bool S_CALLTYPE IHmd_GetWindowBounds(int32_t *pnX, int32_t *pnY, uint32_t *pnWidth, uint32_t *pnHeight) {
	return Hmd()->GetWindowBounds(pnX, pnY, pnWidth, pnHeight);
}

SB_API void S_CALLTYPE IHmd_GetRecommendedRenderTargetSize(uint32_t *pnWidth, uint32_t *pnHeight) {
	return Hmd()->GetRecommendedRenderTargetSize(pnWidth, pnHeight);
}

SB_API void S_CALLTYPE IHmd_GetEyeOutputViewport(vr::Hmd_Eye eEye, vr::GraphicsAPIConvention eAPIType, uint32_t *pnX, uint32_t *pnY, uint32_t *pnWidth, uint32_t *pnHeight) {
	return Hmd()->GetEyeOutputViewport(eEye, eAPIType, pnX, pnY, pnWidth, pnHeight);
}

SB_API vr::HmdMatrix44_t S_CALLTYPE IHmd_GetProjectionMatrix(vr::Hmd_Eye eEye, float fNearZ, float fFarZ, vr::GraphicsAPIConvention eProjType) {
	return Hmd()->GetProjectionMatrix(eEye, fNearZ, fFarZ, eProjType);
}

SB_API void S_CALLTYPE IHmd_GetProjectionRaw(vr::Hmd_Eye eEye, float *pfLeft, float *pfRight, float *pfTop, float *pfBottom) {
	return Hmd()->GetProjectionRaw(eEye, pfLeft, pfRight, pfTop, pfBottom);
}

SB_API vr::DistortionCoordinates_t S_CALLTYPE IHmd_ComputeDistortion(vr::Hmd_Eye eEye, float fU, float fV) {
	return Hmd()->ComputeDistortion(eEye, fU, fV);
}

SB_API vr::HmdMatrix44_t S_CALLTYPE IHmd_GetEyeMatrix(vr::Hmd_Eye eEye) {
	return Hmd()->GetEyeMatrix(eEye);
}

SB_API bool S_CALLTYPE IHmd_GetViewMatrix(float fSecondsFromNow, vr::HmdMatrix44_t *pMatLeftView, vr::HmdMatrix44_t *pMatRightView, vr::HmdTrackingResult *peResult) {
	return Hmd()->GetViewMatrix(fSecondsFromNow, pMatLeftView, pMatRightView, peResult);
}

SB_API int32_t S_CALLTYPE IHmd_GetD3D9AdapterIndex() {
	return Hmd()->GetD3D9AdapterIndex();
}

SB_API bool S_CALLTYPE IHmd_GetWorldFromHeadPose(float fPredictedSecondsFromNow, vr::HmdMatrix34_t *pmPose, vr::HmdTrackingResult *peResult) {
	return Hmd()->GetWorldFromHeadPose(fPredictedSecondsFromNow, pmPose, peResult);
}

SB_API bool S_CALLTYPE IHmd_GetLastWorldFromHeadPose(vr::HmdMatrix34_t *pmPose) {
	return Hmd()->GetLastWorldFromHeadPose(pmPose);
}

SB_API bool S_CALLTYPE IHmd_WillDriftInYaw() {
	return Hmd()->WillDriftInYaw();
}

SB_API void S_CALLTYPE IHmd_ZeroTracker() {
	return Hmd()->ZeroTracker();
}

SB_API uint32_t S_CALLTYPE IHmd_GetDriverId(char *pchBuffer, uint32_t unBufferLen) {
	return Hmd()->GetDriverId(pchBuffer, unBufferLen);
}

SB_API uint32_t S_CALLTYPE IHmd_GetDisplayId(char *pchBuffer, uint32_t unBufferLen) {
	return Hmd()->GetDisplayId(pchBuffer, unBufferLen);
}
