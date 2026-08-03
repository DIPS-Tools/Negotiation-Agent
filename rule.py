from pydantic import BaseModel

from dpv import get_purpose_detail
from odrl import get_action_detail


class Rule(BaseModel): 
    type : str #permission, prohibition, obligation
    query : list[str] #list of dataset.items as a query
    duration : int #days
    action : str #odrl actions: cc:Attribution, cc:CommercialUse, 
        #cc:DerivativeWorks, cc:Distribution, cc:Notice, cc:Reproduction, cc:ShareAlike, 
        # cc:Sharing, cc:SourceCode, odrl:acceptTracking, odrl:adHocShare, odrl:aggregate, 
        # odrl:annotate, odrl:anonymize, odrl:append, odrl:appendTo, odrl:archive, 
        # odrl:attachPolicy, odrl:attachSource, odrl:attribute, odrl:commercialize, 
        # odrl:compensate, odrl:concurrentUse, odrl:copy, odrl:delete, odrl:derive, 
        # odrl:digitize, odrl:display, odrl:distribute, odrl:ensureExclusivity, odrl:execute, 
        # odrl:export, odrl:extract, odrl:extractChar, odrl:extractPage, odrl:extractWord, 
        # odrl:give, odrl:grantUse, odrl:include, odrl:index, odrl:inform, odrl:install, 
        # odrl:lease, odrl:lend, odrl:license, odrl:modify, odrl:move, odrl:nextPolicy, 
        # odrl:obtainConsent, odrl:pay, odrl:play, odrl:present, odrl:preview, odrl:print, 
        # odrl:read, odrl:reproduce, odrl:reviewPolicy, odrl:secondaryUse, odrl:sell, 
        # odrl:share, odrl:shareAlike, odrl:stream, odrl:synchronize, odrl:textToSpeech, 
        # odrl:transfer, odrl:transform, odrl:translate, odrl:uninstall, odrl:use, 
        # odrl:watermark, odrl:write, odrl:writeTo
    purpose : str #dpv pursposes: dpv:AcademicResearch, dpv:AccountManagement, 
    #dpv:Advertising, dpv:AgeVerification, dpv:CombatClimateChange, dpv:CommercialPurpose, 
    # dpv:CommercialResearch, dpv:CommunicationForCustomerCare, dpv:CommunicationManagement, 
    # dpv:CounterMoneyLaundering, dpv:Counterterrorism, dpv:CustomerCare, 
    # dpv:CustomerClaimsManagement, dpv:CustomerManagement, dpv:CustomerOrderManagement, 
    # dpv:CustomerRelationshipManagement, dpv:CustomerSolvencyMonitoring, dpv:DataAltruism, 
    # dpv:DeliveryOfGoods, dpv:DirectMarketing, dpv:DisputeManagement, dpv:EnforceAccessControl, 
    # dpv:EnforceSecurity, dpv:EstablishContractualAgreement, dpv:FraudPreventionAndDetection, 
    # dpv:FulfilmentOfContractualObligation, dpv:FulfilmentOfObligation, 
    # dpv:HumanResourceManagement, dpv:IdentityAuthentication, dpv:IdentityVerification, 
    # dpv:ImproveExistingProductsAndServices, dpv:ImproveHealthcare, 
    # dpv:ImproveInternalCRMProcesses, dpv:ImprovePublicServices, dpv:ImproveTransportAndMobility, 
    # dpv:IncreaseServiceRobustness, dpv:InternalResourceOptimisation, dpv:LegalCompliance, 
    # dpv:MaintainFraudDatabase, dpv:Marketing, dpv:MembersAndPartnersManagement, 
    # dpv:MisusePreventionAndDetection, dpv:NonCommercialPurpose, dpv:NonCommercialResearch, 
    # dpv:OptimisationForConsumer, dpv:OptimisationForController, dpv:OptimiseUserInterface, 
    # dpv:OrganisationComplianceManagement, dpv:OrganisationGovernance, 
    # dpv:OrganisationRiskManagement, dpv:PaymentManagement, dpv:Personalisation, 
    # dpv:PersonalisedAdvertising, dpv:PersonalisedBenefits, dpv:PersonnelBehaviourMonitoring, 
    # dpv:PersonnelHiring, dpv:PersonnelManagement, dpv:PersonnelMonitoring, 
    # dpv:PersonnelOffboarding, dpv:PersonnelOnboarding, dpv:PersonnelPayment, 
    # dpv:PersonnelPerformanceEvaluation, dpv:PersonnelPerformanceManagement, 
    # dpv:PersonnelPerformanceMonitoring, dpv:PersonnelPerformancePrediction, 
    # dpv:PersonnelPromotionManagement, dpv:PersonnelTerminationManagement, 
    # dpv:PersonnelWorkloadManagement, dpv:PoliticalCampaign, 
    # dpv:ProtectionOfIntellectualPropertyRights, dpv:ProtectionOfNationalSecurity, 
    # dpv:ProtectionOfPublicSecurity, dpv:ProvideEventRecommendations, 
    # dpv:ProvideOfficialStatistics, dpv:ProvidePersonalisedRecommendations, 
    # dpv:ProvideProductRecommendations, dpv:PublicBenefit, dpv:PublicPolicyMaking, 
    # dpv:PublicRelations, dpv:Purpose, dpv:RecordManagement, dpv:RecruitmentAdvertising, 
    # dpv:RecruitmentApplicantBackgroundCheck, dpv:RecruitmentApplicantCriminalBackgroundCheck, 
    # dpv:RecruitmentApplicantInformationAuthentication, 
    # dpv:RecruitmentApplicantSelection, dpv:RecruitmentApplicationAnalysis, 
    # dpv:RecruitmentApplicationManagement, dpv:RecruitmentApplicationScreening, 
    # dpv:RecruitmentInterviewAnalysis, dpv:RecruitmentInterviewAssessment, d
    # pv:RecruitmentInterviewManagement, dpv:RecruitmentInterviewScheduling, 
    # dpv:RecruitmentManagement, dpv:TargetedRecruitmentAdvertising, dpv:RepairImpairments, 
    # dpv:RequestedServiceProvision, dpv:ResearchAndDevelopment, dpv:RightsFulfilment, 
    # dpv:ScientificResearch, dpv:SearchFunctionalities, dpv:Sector, dpv:SellDataToThirdParties, 
    # dpv:SellInsightsFromData, dpv:SellProducts, dpv:SellProductsToDataSubject, 
    # dpv:ServiceAccessDetermination, dpv:ServiceManagement, dpv:ServiceMonitoring, 
    # dpv:ServiceOptimisation, dpv:ServicePersonalisation, dpv:ServiceProvision, 
    # dpv:ServiceRegistration, dpv:ServiceUsageAnalytics, dpv:SocialMediaMarketing, 
    # dpv:TargetedAdvertising, dpv:TechnicalServiceProvision, dpv:UserInterfacePersonalisation, 
    # dpv:VendorManagement, dpv:VendorPayment, dpv:VendorRecordsManagement, 
    # dpv:VendorSelectionAssessment, dpv:Verification
    third_party : str #dpv party: google, goverment, ...
    
    
